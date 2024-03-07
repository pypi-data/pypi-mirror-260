from friday.agent.base_agent import BaseAgent
from friday.tool_repository.manager.action_node import ActionNode
from collections import defaultdict, deque
from friday.environment.py_env import PythonEnv
from friday.utils.llms import OpenAI
from friday.tool_repository.manager.tool_manager import ToolManager
from friday.tool_repository.basic_tools.get_os_version import get_os_version, check_os_version
from friday.agent.prompt import prompt
from friday.tool_repository.manager.tool_manager import get_open_api_doc_path, get_open_api_description_pair
import re
import json
import logging
from pathlib import Path

class FridayAgent(BaseAgent):
    """
    An AI agent class that orchestrates the planning, retrieval, and execution of tasks.

    This agent utilizes different modules to handle various aspects of task execution:
    - PlanningModule: Decomposes tasks into subtasks and plans their execution.
    - RetrievalModule: Retrieves necessary tools and codes from the library.
    - ExecutionModule: Executes the planned tasks and manages the execution environment.

    Attributes:
        llm (OpenAI): An instance of the OpenAI language learning model for generating and interpreting tasks.
        tool_lib (ToolManager): Manages the repository of generated tools and code snippets.
        environment (PythonEnv): The execution environment where tasks are performed.
        prompt (dict): A collection of prompts used across different modules for task processing.
        system_version (str): The operating system version, used for tailoring task execution.
        planner (PlanningModule): The module responsible for task planning and decomposition.
        retriever (RetrievalModule): The module for retrieving tools and codes.
        executor (ExecutionModule): The module that executes tasks within the environment.
    """

    def __init__(self, generated_tool_repo_dir=None, max_iter=3):
        """
        Initializes the FridayAgent with necessary components and modules for operation.

        Sets up the language learning model, tool library, and execution environment. Initializes the
        planning, retrieval, and execution modules with appropriate prompts and configurations.

        Args:
            generated_tool_repo_dir (str, optional): The directory for storing generated tools. Defaults to None.
            max_iter (int, optional): The maximum number of iterations for attempting task execution and amendment. Defaults to 3.
        """
        super().__init__()
        self.llm = OpenAI()
        self.tool_lib = ToolManager(generated_tool_repo_dir)
        self.environment = PythonEnv()
        self.prompt = prompt
        self.system_version = get_os_version()
        self.planner = PlanningModule(self.llm, self.environment, self.tool_lib, self.prompt['planning_prompt'], self.system_version)
        self.retriever = RetrievalModule(self.llm, self.environment, self.tool_lib, self.prompt['retrieve_prompt'])
        self.executor = ExecutionModule(self.llm, self.environment, self.tool_lib, self.prompt['execute_prompt'], self.system_version, max_iter)
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)        

    def run(self, task):
        """
        Executes a given task by coordinating between the planning, retrieval, and execution modules.

        This method starts by retrieving tool names and descriptions relevant to the task. It then
        decomposes the task into subtasks, iterates over each subtask, and executes them using the
        appropriate tools or code. It handles task execution, amendment, and replanning as necessary
        based on execution outcomes and errors.

        Args:
            task (str): The high-level task to be executed by the agent.
        """
        # relevant tool 
        retrieve_tool_name = self.retriever.retrieve_tool_name(task)
        retrieve_tool_description_pair = self.retriever.retrieve_tool_description_pair(retrieve_tool_name)

        # decompose task
        self.planner.decompose_task(task, retrieve_tool_description_pair)

        # iter each subtask
        while self.planner.execute_list:
            tool = self.planner.execute_list[0]
            tool_node = self.planner.tool_node[tool]
            description = tool_node.description
            logging.info("The current subtask is: {subtask}".format(subtask=description))
            code = ''
            # The return value of the current task
            result = ''
            next_action = tool_node.next_action
            relevant_code = {}
            type = tool_node.type
            pre_tasks_info = self.planner.get_pre_tasks_info(tool)
            if type == 'Code':
                # retrieve existing tool
                retrieve_name = self.retriever.retrieve_tool_name(description, 3)
                relevant_code = self.retriever.retrieve_tool_code_pair(retrieve_name)
            # task execute step
            if type == 'QA':
                # result = self.executor.question_and_answer_tool(pre_tasks_info, task, task)
                if self.planner.tool_num == 1:
                    result = self.executor.question_and_answer_tool(pre_tasks_info, task, task)
                else:
                    result = self.executor.question_and_answer_tool(pre_tasks_info, task, description)
                print(result)
                logging.info(result)
            else:
                invoke = ''
                if type == 'API':
                    api_path = self.executor.extract_API_Path(description)
                    code = self.executor.api_tool(description, api_path, pre_tasks_info)
                else:
                    code, invoke = self.executor.generate_tool(tool, description, pre_tasks_info, relevant_code)
                # Execute python tool class code
                state = self.executor.execute_tool(code, invoke, type)   
                result = state.result 
                logging.info(state)
            # Check whether the code runs correctly, if not, amend the code
            if type == 'Code':
                need_mend = False
                trial_times = 0
                critique = ''
                score = 0
                # If no error is reported, check whether the task is completed
                if state.error == None:
                    critique, judge, score = self.executor.judge_tool(code, description, state, next_action)
                    if not judge:
                        print("critique: {}".format(critique))
                        need_mend = True
                else:
                    #  Determine whether it is caused by an error outside the code
                    reasoning, error_type = self.executor.analysis_tool(code, description, state)
                    if error_type == 'replan':
                        relevant_tool_name = self.retriever.retrieve_tool_name(reasoning)
                        relevant_tool_description_pair = self.retriever.retrieve_tool_description_pair(relevant_tool_name)
                        self.planner.replan_task(reasoning, tool, relevant_tool_description_pair)
                        continue
                    need_mend = True   
                # The code failed to complete its task, fix the code
                while (trial_times < self.executor.max_iter and need_mend == True):
                    trial_times += 1
                    print("current amend times: {}".format(trial_times))
                    new_code, invoke = self.executor.amend_tool(code, description, state, critique, pre_tasks_info)
                    critique = ''
                    code = new_code
                    # Run the current code and check for errors
                    state = self.executor.execute_tool(code, invoke, type)
                    result = state.result
                    logging.info(state) 
                    # print(state)
                    # Recheck
                    if state.error == None:
                        critique, judge, score = self.executor.judge_tool(code, description, state, next_action)
                        # The task execution is completed and the loop exits
                        if judge:
                            need_mend = False
                            break
                        # print("critique: {}".format(critique))
                    else: # The code still needs to be corrected
                        need_mend = True

                # If the task still cannot be completed, an error message will be reported.
                if need_mend == True:
                    print("I can't Do this Task!!")
                    break
                else: # The task is completed, if code is save the code, args_description, tool_description in lib
                    if score >= 8:
                        self.executor.store_tool(tool, code)
            print("Current task execution completed!!!")  
            self.planner.update_tool(tool, result, relevant_code, True, type)
            self.planner.execute_list.remove(tool)


class PlanningModule(BaseAgent):
    """
    A module responsible for breaking down complex tasks into subtasks, managing re-planning, 
    and organizing the execution flow of tools within a given environment.

    The PlanningModule extends the BaseAgent class, incorporating additional functionality
    for task decomposition, tool planning, and execution management. It utilizes a 
    prompt-based approach with a language model to generate and plan tools based on the 
    current state of the environment and the system's version.
    """
    def __init__(self, llm, environment, tool_lib, prompt, system_version):
        """
        Initializes a new instance of the PlanningModule with the specified parameters.

        This method sets up the planning module by initializing the execution environment, 
        tool library, system version, and prompt. It also initializes structures for 
        managing tool nodes, the tool graph, and the execution list.

        Args:
            llm: The language learning model to be used for planning and task decomposition.
            environment: The current execution environment for the module.
            tool_lib: A collection or library of tools available for planning and execution.
            prompt (str): The initial set of instructions or prompt for the module.
            system_version (str): The version of the system or environment, influencing planning.
        """
        super().__init__()
        # Model, environment, database
        self.llm = llm
        self.environment = environment
        self.tool_lib = tool_lib
        self.system_version = system_version
        self.prompt = prompt
        # tool nodes, tool graph information and tool topology sorting
        self.tool_num = 0
        self.tool_node = {}
        self.tool_graph = defaultdict(list)
        self.execute_list = []

    def decompose_task(self, task, tool_description_pair):
        """
        Decomposes a complex task into manageable subtasks and updates the tool graph.

        This method takes a high-level task and an tool-description pair, and utilizes
        the environment's current state to format and send a decomposition request to the
        language learning model. It then parses the response to construct and update the
        tool graph with the decomposed subtasks, followed by a topological sort to
        determine the execution order.

        Args:
            task (str): The complex task to be decomposed.
            tool_description_pair (dict): A dictionary mapping tool names to their descriptions.

        Side Effects:
            Updates the tool graph with the decomposed subtasks and reorders tools based on
            dependencies through topological sorting.
        """
        files_and_folders = self.environment.list_working_dir()
        tool_description_pair = json.dumps(tool_description_pair)
        response = self.task_decompose_format_message(task, tool_description_pair, files_and_folders)
        logging.info(f"The overall response is: {response}")
        decompose_json = self.extract_json_from_string(response)
        # Building tool graph and topological ordering of tools
        self.create_tool_graph(decompose_json)
        self.topological_sort()

    def replan_task(self, reasoning, current_task, relevant_tool_description_pair):
        """
        Replans the current task by integrating new tools into the original tool graph.

        Given the reasoning for replanning and the current task, this method generates a new
        tool plan incorporating any relevant tools. It formats a replanning request, sends
        it to the language learning model, and integrates the response (new tools) into the
        existing tool graph. The graph is then updated to reflect the new dependencies and
        re-sorted topologically.

        Args:
            reasoning (str): The reasoning or justification for replanning the task.
            current_task (str): The identifier of the current task being replanned.
            relevant_tool_description_pair (dict): A dictionary mapping relevant tool names to
                                                    their descriptions for replanning.

        Side Effects:
            Modifies the tool graph to include new tools and updates the execution order
            of tools within the graph.
        """
        # current_task information
        current_tool = self.tool_node[current_task]
        current_task_description = current_tool.description
        relevant_tool_description_pair = json.dumps(relevant_tool_description_pair)
        files_and_folders = self.environment.list_working_dir()
        response = self.task_replan_format_message(reasoning, current_task, current_task_description, relevant_tool_description_pair, files_and_folders)
        new_tool = self.extract_json_from_string(response)
        # add new tool to tool graph
        self.add_new_tool(new_tool, current_task)
        # update topological sort
        self.topological_sort()

    def update_tool(self, tool, return_val='', relevant_code=None, status=False, type='Code'):
        """
        Updates the specified tool's node information within the tool graph.

        This method allows updating an tool's return value, relevant code, execution status,
        and type. It is particularly useful for modifying tools' details after their execution
        or during the replanning phase.

        Args:
            tool (str): The tool identifier whose details are to be updated.
            return_val (str, optional): The return value of the tool. Default is an empty string.
            relevant_code (str, optional): Any relevant code associated with the tool. Default is None.
            status (bool, optional): The execution status of the tool. Default is False.
            type (str, optional): The type of the tool (e.g., 'Code'). Default is 'Code'.

        Side Effects:
            Updates the information of the specified tool node within the tool graph.
        """
        if return_val:
            if type=='Code':
                return_val = self.extract_information(return_val, "<return>", "</return>")
                print("************************<return>**************************")
                logging.info(return_val)
                print(return_val)
                print("************************</return>*************************")  
            if return_val != 'None':
                self.tool_node[tool]._return_val = return_val
        if relevant_code:
            self.tool_node[tool]._relevant_code = relevant_code
        self.tool_node[tool]._status = status

    def task_decompose_format_message(self, task, tool_list, files_and_folders):
        """
        Formats and sends a decomposition task prompt to the language learning model (LLM) and retrieves a task list.

        This method prepares a message for the LLM by formatting a system and user prompt for task decomposition.
        The message includes details about the system version, the task to be decomposed, available tools,
        API descriptions, the current working directory, and its contents. The formatted message is then sent
        to the LLM to obtain a structured list of decomposed tasks.

        Args:
            task (str): The complex task that needs to be decomposed.
            tool_list (str): A JSON string representing the list of tools available for task decomposition.
            files_and_folders (list): A list of files and folders present in the current working directory.

        Returns:
            The response from the LLM, expected to be a structured list of decomposed tasks.
        """
        api_list = get_open_api_description_pair()
        sys_prompt = self.prompt['_SYSTEM_TASK_DECOMPOSE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_DECOMPOSE_PROMPT'].format(
            system_version=self.system_version,
            task=task,
            tool_list = tool_list,
            api_list = api_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)
      
    def task_replan_format_message(self, reasoning, current_task, current_task_description, tool_list, files_and_folders):
        """
        Formats and sends a replanning task prompt to the language learning model (LLM) and retrieves a task list.

        This method constructs a message for the LLM by incorporating a system and user prompt for task replanning,
        which includes the reasoning for replanning, details of the current task and its description, available tools,
        and the state of the working environment. This message aims to guide the LLM in generating a new set of tools
        or tasks that take into account the provided reasoning and the current state of affairs.

        Args:
            reasoning (str): The justification or reasoning for replanning the current task.
            current_task (str): The identifier of the current task being reconsidered for replanning.
            current_task_description (str): A description of the current task.
            tool_list (str): A JSON string detailing the tools available for replanning.
            files_and_folders (list): A list of the current files and folders in the working directory.

        Returns:
            The response from the LLM, expected to be a new, structured task list that incorporates the given reasoning.
        """
        sys_prompt = self.prompt['_SYSTEM_TASK_REPLAN_PROMPT']
        user_prompt = self.prompt['_USER_TASK_REPLAN_PROMPT'].format(
            current_task = current_task,
            current_task_description = current_task_description,
            system_version=self.system_version,
            reasoning = reasoning,
            tool_list = tool_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def get_tool_list(self, relevant_tool=None):
        """
        Retrieves a list of all tools or a subset of relevant tools, including their names and descriptions.

        This method fetches tool descriptions from the tool library. If a specific set of relevant tools
        is provided, it filters the list to include only those tools. The resulting list (or the full list if
        no relevant tools are specified) is then returned in JSON format.

        Args:
            relevant_tool (list, optional): A list of tool names to filter the returned tools by.
                                            If None, all tools are included. Defaults to None.

        Returns:
            A JSON string representing a dictionary of tool names to their descriptions. 
            The dictionary includes either all tools from the library or only those specified as relevant.
        """
        tool_dict = self.tool_lib.descriptions
        if not relevant_tool:
            return json.dumps(tool_dict)
        relevant_tool_dict = {tool : description for tool ,description in tool_dict.items() if tool in relevant_tool}
        relevant_tool_list = json.dumps(relevant_tool_dict)
        return relevant_tool_list
    
    def create_tool_graph(self, decompose_json):
        """
        Constructs an tool graph based on dependencies specified in the given JSON.

        This method takes a JSON object containing task information and dependencies,
        and constructs an tool graph. Each task is added as a node in the graph, with
        directed edges representing task dependencies. The method updates the class's
        internal structures to reflect this graph, including tool nodes and their
        relationships, as well as the overall number of tools.

        Args:
            decompose_json (dict): A JSON object where each key is an tool name, and the value
                                is a dictionary containing the tool's name, description,
                                type, and dependencies.

        Side Effects:
            Modifies the internal state by updating `tool_num`, `tool_node`, and `tool_graph`
            to reflect the newly created tool graph.
        """
        for _, task_info in decompose_json.items():
            self.tool_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.tool_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.tool_graph[task_name] = task_dependencies
            for pre_tool in self.tool_graph[task_name]:
                self.tool_node[pre_tool].next_action[task_name] = task_description
    
    def add_new_tool(self, new_task_json, current_task):
        """
        Incorporates a new tool into the existing tool graph based on its dependencies.

        This method processes a JSON object representing a new task, including its name,
        description, type, and dependencies, and adds it to the tool graph. It also updates
        the tool nodes to reflect this new addition. Finally, it appends the last new task
        to the list of dependencies for the specified current task.

        Args:
            new_task_json (dict): A JSON object containing the new task's details.
            current_task (str): The name of the current task to which the new task's dependencies will be added.

        Side Effects:
            Updates the tool graph and nodes to include the new tool and its dependencies.
            Modifies the dependencies of the current task to include the new tool.
        """
        for _, task_info in new_task_json.items():
            self.tool_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.tool_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.tool_graph[task_name] = task_dependencies
            for pre_tool in self.tool_graph[task_name]:
                self.tool_node[pre_tool].next_action[task_name] = task_description           
        last_new_task = list(new_task_json.keys())[-1]
        self.tool_graph[current_task].append(last_new_task)

    def topological_sort(self):
        """
        Generates a topological sort of the tool graph to determine the execution order.

        This method applies a topological sorting algorithm to the current tool graph, 
        considering the status of each tool. It aims to identify an order in which tools
        can be executed based on their dependencies, ensuring that all prerequisites are met
        before an tool is executed. The sorting algorithm accounts for tools that have not
        yet been executed to avoid cycles and ensure a valid execution order.

        Side Effects:
            Populates `execute_list` with the sorted order of tools to be executed if a 
            topological sort is possible. Otherwise, it indicates a cycle detection.
        """
        self.execute_list = []
        graph = defaultdict(list)
        for node, dependencies in self.tool_graph.items():
            # If the current node has not been executed, put it in the dependency graph.
            if not self.tool_node[node].status:
                graph.setdefault(node, [])
                for dependent in dependencies:
                    # If the dependencies of the current node have not been executed, put them in the dependency graph.
                    if not self.tool_node[dependent].status:
                        graph[dependent].append(node)

        in_degree = {node: 0 for node in graph}      
        # Count in-degree for each node
        for node in graph:
            for dependent in graph[node]:
                in_degree[dependent] += 1

        # Initialize queue with nodes having in-degree 0
        queue = deque([node for node in in_degree if in_degree[node] == 0])

        # List to store the order of execution

        while queue:
            # Get one node with in-degree 0
            current = queue.popleft()
            self.execute_list.append(current)

            # Decrease in-degree for all nodes dependent on current
            for dependent in graph[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check if topological sort is possible (i.e., no cycle)
        if len(self.execute_list) == len(graph):
            print("topological sort is possible")
        else:
            return "Cycle detected in the graph, topological sort not possible."
        
    def get_pre_tasks_info(self, current_task):
        """
        Retrieves information about the prerequisite tasks for a given current task.

        This method collects and formats details about all tasks that are prerequisites
        for the specified current task. It extracts descriptions and return values for
        each prerequisite task and compiles this information into a JSON string.

        Args:
            current_task (str): The name of the task for which prerequisite information is requested.

        Returns:
            A JSON string representing a dictionary, where each key is a prerequisite task's
            name, and the value is a dictionary with the task's description and return value.
        """
        pre_tasks_info = {}
        for task in self.tool_graph[current_task]:
            task_info = {
                "description" : self.tool_node[task].description,
                "return_val" : self.tool_node[task].return_val
            }
            pre_tasks_info[task] = task_info
        pre_tasks_info = json.dumps(pre_tasks_info)
        return pre_tasks_info



class RetrievalModule(BaseAgent):
    """
    A module within the system responsible for retrieving and managing available tools from the tool library.

    The RetrievalModule extends the BaseAgent class, focusing on the retrieval of tools
    based on specific prompts or queries. It interacts with a language learning model (LLM)
    and utilizes the execution environment and tool library to fulfill its responsibilities.
    """

    def __init__(self, llm, environment, tool_lib, prompt):
        """
        Initializes the RetrievalModule with necessary components for operation.

        This method sets up the module by initializing the execution environment, tool library,
        language learning model (LLM), and prompts used for tool retrieval.

        Args:
            llm: The language learning model used to generate or retrieve tool information.
            environment: The current execution environment where tools are performed.
            tool_lib: A library or collection of tools available for retrieval and execution.
            prompt: Initial set of instructions or prompts used for tool retrieval.
        """
        super().__init__()
        # Model, environment, database
        self.llm = llm
        self.environment = environment
        self.tool_lib = tool_lib
        self.prompt = prompt

    def delete_tool(self, tool):
        """
        Deletes the specified tool from the tool library.

        This method calls the tool library's delete method to remove an tool by its name. It
        encompasses deleting the tool's code, description, parameters, and any other associated
        information.

        Args:
            tool (str): The name of the tool to be deleted.
        """
        self.tool_lib.delete_tool(tool)

    def retrieve_tool_name(self, task, k=10):        
        """
        Retrieves a list of tool names relevant to the specified task.

        This method interacts with the tool library to retrieve names of tools that are most
        relevant to a given task. The number of tool names returned is limited by the parameter k.

        Args:
            task (str): The task for which relevant tool names are to be retrieved.
            k (int, optional): The maximum number of tool names to retrieve. Defaults to 10.

        Returns:
            list[str]: A list of the top k tool names relevant to the specified task.
        """
        retrieve_tool_name = self.tool_lib.retrieve_tool_name(task, k)
        return retrieve_tool_name

    def tool_code_filter(self, tool_code_pair, task):
        """
        Filters and retrieves the code for an tool relevant to the specified task.

        This method formats a message for filtering tool codes based on a given task, sends
        the message to the tool library for processing, and retrieves the filtered tool's
        code. If an tool name is successfully identified, its corresponding code is fetched
        from the tool library.

        Args:
            tool_code_pair (dict): A dictionary mapping tool names to their codes.
            task (str): The task based on which the tool code needs to be filtered.

        Returns:
            The code of the tool relevant to the specified task, or an empty string
            if no relevant tool is found.
    """
        tool_code_pair = json.dumps(tool_code_pair)
        response = self.tool_code_filter_format_message(tool_code_pair, task)
        tool_name = self.extract_information(response, '<action>', '</action>')[0]
        code = ''
        if tool_name:
            code = self.tool_lib.get_tool_code(tool_name)
        return code

    def retrieve_tool_description(self, tool_name):
        """
        Retrieves the description for a specified tool from the tool library.

        This method queries the tool library for the description of an tool identified
        by its name. It is designed to fetch detailed descriptions that explain what the
        tool does.

        Args:
            tool_name (str): The name of the tool whose description is to be retrieved.

        Returns:
            str: The description of the specified tool.
        """
        retrieve_tool_description = self.tool_lib.retrieve_tool_description(tool_name)
        return retrieve_tool_description  

    def retrieve_tool_code(self, tool_name):
        """
        Retrieves the code for a specified tool from the tool library.

        This method accesses the tool library to get the executable code associated with
        an tool identified by its name. This code defines how the tool is performed.

        Args:
            tool_name (str): The name of the tool whose code is to be retrieved.

        Returns:
            str: The code of the specified tool.
        """
        retrieve_tool_code = self.tool_lib.retrieve_tool_code(tool_name)
        return retrieve_tool_code 
    
    def retrieve_tool_code_pair(self, retrieve_tool_name):
        """
        Retrieves a mapping of tool names to their respective codes for a list of tools.

        This method processes a list of tool names, retrieving the code for each and
        compiling a dictionary that maps each tool name to its code. This is useful for
        tasks that require both the identification and the execution details of tools.

        Args:
            retrieve_tool_name (list[str]): A list of tool names for which codes are to be retrieved.

        Returns:
            dict: A dictionary mapping each tool name to its code.
        """
        retrieve_tool_code = self.retrieve_tool_code(retrieve_tool_name)
        tool_code_pair = {}
        for name, description in zip(retrieve_tool_name, retrieve_tool_code):
            tool_code_pair[name] = description
        return tool_code_pair        
        
    def retrieve_tool_description_pair(self, retrieve_tool_name):
        """
        Retrieves a mapping of tool names to their descriptions for a list of tools.

        By processing a list of tool names, this method fetches their descriptions and
        forms a dictionary that associates each tool name with its description. This
        facilitates understanding the purpose and functionality of multiple tools at once.

        Args:
            retrieve_tool_name (list[str]): A list of tool names for which descriptions are to be retrieved.

        Returns:
            dict: A dictionary mapping each tool name to its description.
        """
        retrieve_tool_description = self.retrieve_tool_description(retrieve_tool_name)
        tool_description_pair = {}
        for name, description in zip(retrieve_tool_name, retrieve_tool_description):
            tool_description_pair[name] = description
        return tool_description_pair
    
    def tool_code_filter_format_message(self, tool_code_pair, task_description):
        """
        Formats and sends a message to the language learning model (LLM) to filter out irrelevant tool codes.

        This method constructs a message comprising system and user prompts intended for the LLM, aimed at
        filtering unnecessary or irrelevant tool codes based on the provided task description. The message
        includes the task description and a pairing of tool names to their respective codes. The formatted
        message is then sent to the LLM for processing, expecting the LLM to return a filtered list of tool
        codes that are relevant to the task at hand.

        Args:
            tool_code_pair (str): A JSON string representing a dictionary mapping tool names to their codes.
            task_description (str): The description of the current task for which relevant tool codes need to be filtered.

        Returns:
            The response from the LLM, expected to include only the tool codes relevant to the specified task.
        """
        sys_prompt = self.prompt['_SYSTEM_ACTION_CODE_FILTER_PROMPT']
        user_prompt = self.prompt['_USER_ACTION_CODE_FILTER_PROMPT'].format(
            task_description=task_description,
            tool_code_pair=tool_code_pair
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    


class ExecutionModule(BaseAgent):
    """
    A module within the system responsible for executing tools based on prompts and maintaining the tool library.

    The ExecutionModule extends the BaseAgent class, focusing on the practical execution of tools determined
    by the system. It utilizes a language learning model (LLM) in conjunction with an execution environment and
    an tool library to carry out tools. Additionally, it manages system versioning and prompt initialization
    for tool execution guidance.
    """

    def __init__(self, llm, environment, tool_lib, prompt, system_version, max_iter):
        """
        Initializes the ExecutionModule with the necessary components for operation.

        This constructor sets up the module by initializing the execution environment, the tool library,
        the language learning model (LLM), prompts for execution, system version, and the maximum number of
        iterations allowed. It also loads the OpenAPI documentation from a specified path into a dictionary
        for quick access during execution.

        Args:
            llm: The language learning model to be used for execution guidance.
            environment: The current execution environment for the module.
            tool_lib: A collection or library of tools available for execution.
            prompt (str): The initial set of instructions or prompts for guiding tool execution.
            system_version (str): The version of the system or environment, influencing execution strategies.
            max_iter (int): The maximum number of iterations the module can perform.
        """
        super().__init__()
        self.llm = llm
        self.environment = environment
        self.tool_lib = tool_lib
        self.system_version = system_version
        self.prompt = prompt
        self.max_iter = max_iter
        self.open_api_doc_path = get_open_api_doc_path()
        self.open_api_doc = {}
        with open(self.open_api_doc_path) as f:
            self.open_api_doc = json.load(f) 
    
    def generate_tool(self, task_name, task_description, pre_tasks_info, relevant_code):
        """
        Generates executable code and invocation logic for a specified tool.

        This method constructs a message to generate tool code capable of completing the specified task,
        taking into account any prerequisite task information and relevant code snippets. It then formats
        this message for processing by the language learning model (LLM) to generate the tool code. The
        method extracts the executable Python code and the specific invocation logic from the LLM's response.

        Args:
            task_name (str): The name of the task for which tool code is being generated.
            task_description (str): A description of the task, detailing what the tool aims to accomplish.
            pre_tasks_info (dict): Information about tasks that are prerequisites for the current task, including their descriptions and return values.
            relevant_code (dict): A dictionary of code snippets relevant to the current task, possibly including code from prerequisite tasks.

        Returns:
            tuple: A tuple containing two elements:
                - code (str): The generated Python code for the tool.
                - invoke (str): The specific logic or command to invoke the generated tool.

        Note:
            The method relies on the LLM's ability to interpret the provided task context and generate
            syntactically correct Python code and invocation logic based on the `skill_create_and_invoke_format_message`
            method's output.
        """
        relevant_code = json.dumps(relevant_code)
        create_msg = self.skill_create_and_invoke_format_message(task_name, task_description, pre_tasks_info, relevant_code)
        code = self.extract_python_code(create_msg)
        invoke = self.extract_information(create_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return code, invoke

    def execute_tool(self, code, invoke, type):
        """
        Executes a given tool code and returns the execution state.

        This method handles the execution of tool code based on its type. For code tools, it appends
        additional instructions to print the execution result within designated markers. It then passes
        the modified code for execution in the environment. The method captures and prints the execution
        state, including any results or errors, and returns this state.

        Args:
            code (str): The Python code to be executed as part of the tool.
            invoke (str): The specific command or function call that triggers the tool within the code.
            type (str): The type of the tool, determining how the tool is executed. Currently supports 'Code' type.

        Returns:
            state: The state object returned by the environment after executing the tool. This object contains
                   details about the execution's outcome, including any results or errors.

        Note:
            The execution logic is currently tailored for tools of type 'Code', where the code is directly executable
            Python code. The method is designed to be extensible for other tool types as needed.
        """
        # print result info
        if type == 'Code':
            info = "\n" + '''print("<return>")''' + "\n" + "print(result)" +  "\n" + '''print("</return>")'''
            code = code + '\nresult=' + invoke + info
        print("************************<code>**************************")
        print(code)
        print("************************</code>*************************")  
        state = self.environment.step(code)
        print("************************<state>**************************")
        print(state)
        # print("error: " + state.error + "\nresult: " + state.result + "\npwd: " + state.pwd + "\nls: " + state.ls)
        print("************************</state>*************************") 
        return state

    def judge_tool(self, code, task_description, state, next_action):
        """
        Evaluates the outcome of an executed tool to determine its success in completing a task.

        This method formulates and sends a judgment request to the language learning model (LLM) based on the
        executed tool's code, the task description, the execution state, and the expected next tool. It
        then parses the LLM's response to determine the tool's success, providing reasoning, a judgment (boolean),
        and a score that quantifies the tool's effectiveness.

        Args:
            code (str): The code of the tool that was executed.
            task_description (str): The description of the task the tool was intended to complete.
            state: The state object returned by the environment after executing the tool, containing execution results.
            next_action (str): The name of the next expected tool in the sequence.

        Returns:
            tuple: A tuple containing:
                - reasoning (str): The LLM's reasoning behind the judgment.
                - judge (bool): The LLM's judgment on whether the tool successfully completed the task.
                - score (float): A score representing the effectiveness of the tool.
        """
        judge_json = self.task_judge_format_message(code, task_description, state.result, state.pwd, state.ls, next_action)
        reasoning = judge_json['reasoning']
        judge = judge_json['judge']
        score = judge_json['score']
        return reasoning, judge, score

    def amend_tool(self, current_code, task_description, state, critique, pre_tasks_info):
        """
        Modifies or corrects the code of an tool based on feedback to better complete a task.

        This method sends an amendment request to the LLM, including details about the current code, task description,
        execution state, critique of the tool's outcome, and information about prerequisite tasks. It aims to generate
        a revised version of the code that addresses any identified issues or incomplete aspects of the task. The method
        extracts and returns both the amended code and the specific logic or command to invoke the amended tool.

        Args:
            current_code (str): The original code of the tool that requires amendment.
            task_description (str): The description of the task the tool is intended to complete.
            state: The state object containing details about the tool's execution outcome.
            critique (str): Feedback or critique on the tool's execution, used to guide the amendment.
            pre_tasks_info (dict): Information about tasks that are prerequisites for the current task.

        Returns:
            tuple: A tuple containing:
                - new_code (str): The amended code for the tool.
                - invoke (str): The command or logic to invoke the amended tool.
        """
        amend_msg = self.skill_amend_and_invoke_format_message(current_code, task_description, state.error, state.result, state.pwd, state.ls, critique, pre_tasks_info)
        new_code = self.extract_python_code(amend_msg)
        invoke = self.extract_information(amend_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return new_code, invoke

    def analysis_tool(self, code, task_description, state):
        """
        Analyzes the execution outcome of an tool to determine the nature of any errors.

        This method evaluates the execution state of an tool, specifically looking for errors. Based on the
        analysis, it determines whether the error is environmental and requires new operations (handled by the
        planning module) or is amendable via the `amend_tool` method. The analysis results, including the reasoning
        and error type, are returned in JSON format.

        Args:
            code (str): The code that was executed for the tool.
            task_description (str): The description of the task associated with the tool.
            state: The state object containing the result of the tool's execution, including any errors.

        Returns:
            tuple: A tuple containing:
                - reasoning (str): The analysis's reasoning regarding the nature of the error.
                - type (str): The type of error identified ('environmental' for new operations, 'amendable' for corrections).
        """
        analysis_json = self.error_analysis_format_message(code, task_description, state.error, state.pwd, state.ls)
        reasoning = analysis_json['reasoning']
        type = analysis_json['type']
        return reasoning, type
        
    def store_tool(self, tool, code):
        """
        Stores the provided tool and its code in the tool library.

        If the specified tool does not already exist in the tool library, this method proceeds to store the tool's
        code, arguments description, and other relevant information. It involves saving these details into JSON files and
        updating the tool library database. If the tool already exists, it outputs a notification indicating so.

        Args:
            tool (str): The name of the tool to be stored.
            code (str): The executable code associated with the tool.

        Side Effects:
            - Adds a new tool to the tool library if it doesn't already exist.
            - Saves tool details to the filesystem and updates the tool library's database.
            - Outputs a message if the tool already exists in the library.
        """
        # If tool not in db.
        if not self.tool_lib.exist_tool(tool):
            # Implement tool storage logic and store new tools
            args_description = self.extract_args_description(code)
            tool_description = self.extract_tool_description(code)
            # Save tool name, code, and description to JSON
            tool_info = self.save_tool_info_to_json(tool, code, tool_description)
            # Save code and descriptions to databases and JSON files
            self.tool_lib.add_new_tool(tool_info)
            # Parameter description save path
            args_description_file_path = self.tool_lib.tool_lib_dir + '/args_description/' + tool + '.txt'      
            # save args_description
            self.save_str_to_path(args_description, args_description_file_path)
        else:
            print("tool already exists!")

    def api_tool(self, description, api_path, context="No context provided."):
        """
        Executes a task by calling an API tool with the provided description and context.

        This method formats a message to generate executable code for an API call based on the
        provided description and context. It sends this message to the language learning model (LLM),
        extracts the executable Python code from the LLM's response, and returns this code.

        Args:
            description (str): A description of the task to be performed by the API call.
            api_path (str): The path or endpoint of the API to be called.
            context (str, optional): Additional context to be included in the API call. Defaults to "No context provided.".

        Returns:
            str: The generated Python code to execute the API call.
        """
        response = self.generate_call_api_format_message(description, api_path, context)
        code = self.extract_python_code(response)
        return code 
    
    def question_and_answer_tool(self, context, question, current_question=None):
        """
        Generates an answer to a given question based on the provided context.

        This method formats a question-and-answer message, incorporating the given context and question,
        and optionally a current question for further clarification. It sends this message to the LLM,
        which processes the information and returns an appropriate response based on the context.

        Args:
            context (str): The context or background information relevant to the question.
            question (str): The question to which an answer is sought.
            current_question (str, optional): An additional question for context or clarification. Defaults to None.

        Returns:
            The response from the LLM providing an answer based on the given context and question.
        """
        response = self.question_and_answer_format_message(context, question, current_question)
        return response

    def skill_create_and_invoke_format_message(self, task_name, task_description, pre_tasks_info, relevant_code):
        """
        Formats and sends a message to the LLM to generate and invoke a skill for a specific task.

        This method constructs a detailed prompt for the LLM, including system version, task description,
        working directory, task name, information on prerequisite tasks, and any relevant code snippets.
        The prompt aims to guide the LLM in generating a new skill (tool) that can accomplish the task,
        along with the invocation logic. The formatted message is then sent to the LLM for processing.

        Args:
            task_name (str): The name of the task for which a skill is to be generated and invoked.
            task_description (str): A description of the task, providing details on what needs to be accomplished.
            pre_tasks_info (str): Information about prerequisite tasks that may influence the new skill's creation.
            relevant_code (str): Code snippets relevant to the task that may assist in skill generation.

        Returns:
            The response from the LLM, expected to include both the generated skill (tool code) and its invocation logic.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_AND_INVOKE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name,
            pre_tasks_info=pre_tasks_info,
            relevant_code=relevant_code
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def skill_create_format_message(self, task_name, task_description):
        """
        Formats and sends a message to the LLM to generate code for a new skill based on a given task.

        This method creates a detailed prompt including the system version, task description, current working
        directory, and task name, aiming to guide the LLM in generating code for a new skill that accomplishes
        the specified task. The formatted message is sent to the LLM for processing.

        Args:
            task_name (str): The name of the task for which a new skill is to be generated.
            task_description (str): A description of the task, outlining what the new skill needs to accomplish.

        Returns:
            The response from the LLM, expected to include the generated code for the new skill.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def invoke_generate_format_message(self, class_code, task_description, pre_tasks_info):
        """
        Formats and sends a message to the LLM to generate invocation logic for a given class code.

        This method prepares a prompt for the LLM that includes the name of the class, its description,
        information about its arguments (extracted from the class code), the task description, information
        on prerequisite tasks, and the current working directory. The goal is to have the LLM generate
        invocation logic for the class that aligns with the provided task requirements.

        Args:
            class_code (str): The code of the class for which invocation logic is to be generated.
            task_description (str): The description of the task the class is intended to perform.
            pre_tasks_info (str): Information about tasks that are prerequisites for the current task.

        Returns:
            The response from the LLM, expected to include the generated invocation logic for the class.
        """
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        sys_prompt = self.prompt['_SYSTEM_INVOKE_GENERATE_PROMPT']
        user_prompt = self.prompt['_USER_INVOKE_GENERATE_PROMPT'].format(
            class_name = class_name,
            task_description = task_description,
            args_description = args_description,
            pre_tasks_info = pre_tasks_info,
            working_dir = self.environment.working_dir
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)        
    
    def question_and_answer_format_message(self, context, question, current_question):
        """
        Formats and sends a question and answer (Q&A) message to the language learning model (LLM).

        This method constructs a message for the LLM, designed to facilitate answering a given question
        within a specified context. The message includes system and user prompts that detail the context,
        the primary question, and any current or follow-up question for clarification.

        Args:
            context (str): The context or background information relevant to the question.
            question (str): The main question to which an answer is sought.
            current_question (str): A current or follow-up question that may provide additional clarification.

        Returns:
            The response from the LLM, expected to provide an answer to the question within the given context.
        """
        sys_prompt = self.prompt['_SYSTEM_QA_PROMPT']
        user_prompt = self.prompt['_USER_QA_PROMPT'].format(
            context = context,
            question = question,
            current_question = current_question
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)      
 
    def skill_amend_and_invoke_format_message(self, original_code, task, error, code_output, current_working_dir, files_and_folders, critique, pre_tasks_info):
        """
        Formats and sends a skill amendment and invocation message to the LLM.

        This method prepares a message aimed at amending and invoking a skill based on original code
        that encountered an error. The message includes detailed prompts about the task, encountered error,
        expected code output, current working directory, and critiques of the original code. It aims to guide
        the LLM in generating amended code that addresses the error and aligns with the task requirements.

        Args:
            original_code (str): The original code that requires amendment.
            task (str): The task associated with the code.
            error (str): The error encountered during the execution of the original code.
            code_output (str): The expected output of the code, if known.
            current_working_dir (str): The current working directory path.
            files_and_folders (list): A list of files and folders present in the current working directory.
            critique (str): A critique or feedback on the original code, providing insights for amendment.
            pre_tasks_info (str): Information about tasks that are prerequisites for the current task.

        Returns:
            The response from the LLM, expected to include amended code and invocation logic that rectifies the identified issues.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_AND_INVOKE_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            current_working_dir = current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders = files_and_folders,
            critique = critique,
            pre_tasks_info = pre_tasks_info
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)   

    def skill_amend_format_message(self, original_code, task, error, code_output, current_working_dir, files_and_folders, critique):
        """
        Formats and sends a skill amendment message to the LLM for code correction.

        This method constructs a detailed prompt for the LLM to amend the provided original code based on
        the specified task, identified error, expected code output, critique, and the current working environment.
        The aim is to guide the LLM in generating a corrected version of the code that addresses the identified
        issues and aligns with the task requirements.

        Args:
            original_code (str): The original code snippet that requires amendment.
            task (str): The task or objective the code aims to achieve.
            error (str): The error encountered during the original code execution.
            code_output (str): The expected output from the corrected code, if known.
            current_working_dir (str): The current working directory during code execution.
            files_and_folders (list): A list detailing the files and folders within the current working directory.
            critique (str): Feedback or critique on the original code, providing guidance for amendments.

        Returns:
            The response from the LLM, expected to provide corrected code based on the amendment request.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            current_working_dir = current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders = files_and_folders,
            critique = critique
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    
    
    def task_judge_format_message(self, current_code, task, code_output, current_working_dir, files_and_folders, next_action):
        """
        Formats and sends a task judgment prompt to the LLM to evaluate the execution outcome.

        This method prepares a message for the LLM to judge whether the current code successfully
        accomplishes the specified task, considering the code's output and the next expected tool.
        The prompt includes details of the task, the code's execution environment, and any relevant
        next tools. The method aims to obtain a JSON response from the LLM that provides an evaluation
        of the code's success in completing the task.

        Args:
            current_code (str): The code being judged for task completion.
            task (str): The task or objective associated with the code.
            code_output (str): The output produced by executing the current code.
            current_working_dir (str): The directory in which the code was executed.
            files_and_folders (list): The files and folders present in the current working directory.
            next_action (dict): A JSON-serializable dictionary detailing the next expected tool after the current code execution.

        Returns:
            dict: A JSON object representing the LLM's judgment on the code's success in completing the task, including reasoning and evaluation metrics.
        """
        next_action = json.dumps(next_action)
        sys_prompt = self.prompt['_SYSTEM_TASK_JUDGE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_JUDGE_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_output=code_output,
            current_working_dir=current_working_dir,
            working_dir=self.environment.working_dir,
            files_and_folders=files_and_folders,
            next_action=next_action
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response =self.llm.chat(self.message)
        judge_json = self.extract_json_from_string(response)  
        print("************************<judge_json>**************************")
        print(judge_json)
        print("************************</judge_json>*************************")           
        return judge_json    

    def error_analysis_format_message(self, current_code, task, code_error, current_working_dir, files_and_folders):
        """
        Formats and sends an error analysis prompt to the language learning model (LLM) and retrieves a JSON response.

        This method constructs a detailed prompt for the LLM, designed to analyze errors in executed code. The prompt includes
        the current code snippet, task description, encountered error, the current working directory, and a list of files and
        folders present. It aims to receive a JSON response from the LLM that provides insights into the error and potential
        solutions or analysis.

        Args:
            current_code (str): The code snippet that encountered an error.
            task (str): The task description associated with the code.
            code_error (str): The error message or description from the code execution.
            current_working_dir (str): The path of the current working directory.
            files_and_folders (list): A list detailing the files and folders present in the current working directory.

        Returns:
            dict: A JSON object containing the LLM's analysis of the error, potentially including insights and solutions.
        """
        sys_prompt = self.prompt['_SYSTEM_ERROR_ANALYSIS_PROMPT']
        user_prompt = self.prompt['_USER_ERROR_ANALYSIS_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_error=code_error,
            current_working_dir=current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders= files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response =self.llm.chat(self.message)
        analysis_json = self.extract_json_from_string(response)      
        print("************************<analysis_json>**************************")
        print(analysis_json)
        print("************************</analysis_json>*************************")           
        return analysis_json  

    def extract_python_code(self, response):
        """
        Extracts Python code snippets from a response string that includes code block markers.

        This method parses a response string to extract Python code enclosed within '```python' and '```' markers.
        It's designed to retrieve executable Python code snippets from formatted responses, such as those returned
        by a language learning model after processing a code generation or analysis prompt.

        Args:
            response (str): The response string containing the Python code block to be extracted.

        Returns:
            str: The extracted Python code snippet, or an empty string if no code block is found.
        """
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code    

    def extract_class_name_and_args_description(self, class_code):
        """
        Extracts the class name and arguments description from a given Python class code.

        This method searches the provided class code for the class name and the documentation string
        of the `__call__` method, which typically includes descriptions of the arguments. It uses regular
        expressions to locate these elements within the code.

        Args:
            class_code (str): The Python code of the class from which information is to be extracted.

        Returns:
            tuple: A tuple containing:
                - class_name (str): The name of the class extracted from the code.
                - args_description (str): The arguments description extracted from the `__call__` method's docstring, if available; otherwise, None.
        """
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, args_description
    
    def extract_args_description(self, class_code):
        """
        Extracts the arguments description from the `__call__` method's docstring within Python class code.

        This method specifically targets the docstring of the `__call__` method in a class, which is conventionally
        used to describe the method's parameters. The extraction is performed using a regular expression that
        captures the content of the docstring.

        Args:
            class_code (str): The Python code of the class from which the arguments description is to be extracted.

        Returns:
            str: The extracted arguments description from the `__call__` method's docstring, or None if the docstring is not found or does not contain descriptions.
        """
        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None
        return args_description

    def extract_tool_description(self, class_code):
        """
        Extracts the description of an tool from the class's initialization method in Python code.

        This method looks for the tool's description assigned to `self._description` within the `__init__` method
        of a class. It uses regular expressions to find this assignment and extracts the description string. This
        approach assumes that the tool's description is directly assigned as a string literal to `self._description`.

        Args:
            class_code (str): The complete Python code of the class from which the tool description is to be extracted.

        Returns:
            str: The extracted description of the tool if found; otherwise, None.
        """
        init_pattern = r"def __init__\s*\(self[^)]*\):\s*(?:.|\n)*?self\._description\s*=\s*\"([^\"]+)\""
        tool_match = re.search(init_pattern, class_code, re.DOTALL)
        tool_description = tool_match.group(1).strip() if tool_match else None
        return tool_description
    
    def save_str_to_path(self, content, path):
        """
        Saves a string content to a file at the specified path, ensuring the directory exists.

        This method takes a string and a file path, creating any necessary parent directories before
        writing the content to the file. It ensures that the content is written with proper encoding and
        that any existing content in the file is overwritten. The content is processed to remove extra
        whitespace at the beginning and end of each line before saving.

        Args:
            content (str): The string content to be saved to the file.
            path (str): The filesystem path where the content should be saved. If the directory does not exist,
                        it will be created.

        Side Effects:
            - Creates the directory path if it does not exist.
            - Writes the content to a file at the specified path, potentially overwriting existing content.
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            lines = content.strip().splitlines()
            content = '\n'.join(lines)
            f.write(content)
                 
    def save_tool_info_to_json(self, tool, code, description):
        """
        Constructs a dictionary containing tool information suitable for JSON serialization.

        This method packages the name, code, and description of an tool into a dictionary, making it ready
        for serialization or further processing. This structured format is useful for saving tool details
        in a consistent manner, facilitating easy storage and retrieval.

        Args:
            tool (str): The name of the tool.
            code (str): The executable code associated with the tool.
            description (str): A textual description of what the tool does.

        Returns:
            dict: A dictionary containing the tool's name, code, and description.
        """
        info = {
            "task_name" : tool,
            "code": code,
            "description": description
        }
        return info
    
    def generate_call_api_format_message(self, tool_sub_task, tool_api_path, context="No context provided."):
        """
        Formats and sends a message to the LLM for generating API call code based on a specified task and API path.

        This method constructs a system prompt that includes an OpenAPI documentation snippet (generated from
        the provided API path), the sub-task description, and additional context. This formatted message is aimed
        at guiding the LLM to generate executable code that performs an API call relevant to the specified tool
        sub-task. The message includes both system and user roles for comprehensive context provision.

        Args:
            tool_sub_task (str): The specific sub-task or function the API call aims to perform.
            tool_api_path (str): The path or endpoint of the API for which the call code is to be generated.
            context (str, optional): Additional context to aid in code generation. Defaults to "No context provided.".

        Returns:
            The response from the LLM, expected to include the generated code for the API call.
        """
        self.sys_prompt = self.prompt['_SYSTEM_TOOL_USAGE_PROMPT'].format(
            openapi_doc = json.dumps(self.generate_openapi_doc(tool_api_path)),
            tool_sub_task = tool_sub_task,
            context = context
        )
        self.user_prompt = self.prompt['_USER_TOOL_USAGE_PROMPT']
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)
    
    def generate_openapi_doc(self, tool_api_path):
        """
        Generates a formatted OpenAPI document for a specific API path.

        This method constructs a simplified OpenAPI document focused on the specified tool API path.
        It initializes the document with the general OpenAPI, info, and components schemas from the
        module's overall OpenAPI documentation, then selectively adds details for the given API path.
        If the tool API path does not exist in the original OpenAPI document, an error message is
        returned instead.

        Args:
            tool_api_path (str): The specific API path for which to generate the OpenAPI documentation.

        Returns:
            dict: A dictionary representing the formatted OpenAPI documentation for the specified API path or an error message if the path does not exist in the module's OpenAPI documentation.
        """
        # init current api's doc
        curr_api_doc = {}
        curr_api_doc["openapi"] = self.open_api_doc["openapi"]
        curr_api_doc["info"] = self.open_api_doc["info"]
        curr_api_doc["paths"] = {}
        curr_api_doc["components"] = {"schemas":{}}
        api_path_doc = {}
        #extract path and schema
        if tool_api_path not in self.open_api_doc["paths"]:
            curr_api_doc = {"error": "The api is not existed"}
            return curr_api_doc
        api_path_doc = self.open_api_doc["paths"][tool_api_path]
        curr_api_doc["paths"][tool_api_path] = api_path_doc
        find_ptr = {}
        if "get" in api_path_doc:
            findptr  = api_path_doc["get"]
        elif "post" in api_path_doc:
            findptr = api_path_doc["post"]
        api_params_schema_ref = ""
        # json格式
        if (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("application/json" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["application/json"]) and 
        ("$ref" in findptr["requestBody"]["content"]["application/json"]["schema"])):
            api_params_schema_ref = findptr["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        elif (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("multipart/form-data" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["multipart/form-data"]) and 
        ("allOf" in findptr["requestBody"]["content"]["multipart/form-data"]["schema"]) and 
        ("$ref" in findptr["requestBody"]["content"]["multipart/form-data"]["schema"]["allOf"][0])):
            api_params_schema_ref = findptr["requestBody"]["content"]["multipart/form-data"]["schema"]["allOf"][0]["$ref"]
        if api_params_schema_ref != None and api_params_schema_ref != "":
            curr_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]] = self.open_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]]
        return curr_api_doc

    def extract_API_Path(self, text):
        """
        Extracts both UNIX-style and Windows-style file paths from the provided text string.

        This method applies regular expressions to identify and extract file paths that may be present in
        the input text. It is capable of recognizing paths that are enclosed within single or double quotes
        and supports both UNIX-style paths (e.g., `/home/user/docs`) and Windows-style paths (e.g., `C:\\Users\\user\\docs`).
        If multiple paths are found, only the first match is returned, following the function's current implementation.

        Args:
            text (str): The string from which file paths are to be extracted.

        Returns:
            str: The first file path found in the input text, with any enclosing quotes removed. If no paths are
                found, an empty string is returned.

        Note:
            The current implementation returns only the first extracted path. If multiple paths are present in the
            input text, consider modifying the method to return all found paths if the use case requires it.
        """
        # Regular expression for UNIX-style and Windows-style paths
        unix_path_pattern = r"/[^/\s]+(?:/[^/\s]*)*"
        windows_path_pattern = r"[a-zA-Z]:\\(?:[^\\\/\s]+\\)*[^\\\/\s]+"

        # Combine both patterns
        pattern = f"({unix_path_pattern})|({windows_path_pattern})"

        # Find all matches
        matches = re.findall(pattern, text)

        # Extract paths from the tuples returned by findall
        paths = [match[0] or match[1] for match in matches]

        # Remove enclosing quotes (single or double) from the paths
        stripped_paths = [path.strip("'\"") for path in paths]
        return stripped_paths[0]



if __name__ == '__main__':
    agent = FridayAgent(config_path='../../examples/config.json', tool_lib_dir="friday/tool_repository/generated_tools")
    print(agent.executor.extract_API_Path('''Use the "/tools/arxiv' API to search for the autogen paper and retrieve its summary.'''))
