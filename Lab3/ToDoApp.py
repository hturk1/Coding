class ToDoModel:
    def __init__(self):
        self.tasks = [] # Initialize an empty list to store tasks

    def add_task(self, task):
        self.tasks.append(task) # Add a task to the list

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index] # Delete the task at the specified index
        
    def get_tasks(self):
        return self.tasks # Return the list of tasks
    
class ToDoView:
    def print_todo_list(self, tasks):
        print("\nTo-Do List:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}") # Print each task with its index

    def sort_todo_list(self, tasks):
        sorted_tasks = sorted(tasks) # Sort the tasks alphabetically
        self.print_todo_list(sorted_tasks) # Print the sorted to-do list
            
class ToDoController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    def add_task(self, task):
        self.model.add_task(task) # Call the model to add a task

    def delete_task(self, task_index):
        self.model.delete_task(task_index) # Call the model to delete a task

    def display_todo_list(self):
        tasks = self.model.get_tasks() # Retrieve the list of tasks from the model
        self.view.print_todo_list(tasks) # Call the view to display the list

    def sort_todo_list(self):
        tasks = self.model.get_tasks() # Retrieve the list of tasks from the model
        self.view.sort_todo_list(tasks) # Call the view to sort and display the list

def main():
    model = ToDoModel()
    view = ToDoView()
    controller = ToDoController(model, view)

    controller.add_task("Go shopping")
    controller.add_task("Complete work project")
    controller.add_task("Attend school meeting")
    
#   Display the initial To-Do list
    controller.display_todo_list()

#   Sort and display the To-Do list
#   controller.sort_todo_list()
    
#   Delete a task (e.g., the second task, index 1)
#   controller.delete_task(1)
    
#   Display the updated To-Do list after deletion
#   controller.display_todo_list()
    
if __name__ == "__main__":
    main()
