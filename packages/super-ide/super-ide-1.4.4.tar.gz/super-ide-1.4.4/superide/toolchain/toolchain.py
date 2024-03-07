import json
import subprocess

class Toolchain:
    def __init__(self, image_name, project_directory):
        self.image_name = image_name
        self.project_directory = project_directory
        self.contain_project_directory = "/app/project"
        self.check_image()
        self._get_tools()
        
    def check_image(self):
        try:
            output = subprocess.check_output(["docker", "images", "-q", self.image_name])
            if output:
                return
            else:
                print(f"The image '{self.image_name}' does not exist locally.")
                # 拉取镜像
                subprocess.run(['docker', 'pull', self.image_name])


        except subprocess.CalledProcessError:
            print("Failed to execute the command.")


    def _get_tools(self):
        with open(f'{self.project_directory}/.vscode/tasks.json') as file:
            config = json.load(file)
        for task in config['tasks']:
            if task['label'] == 'Build':
                self.build_task = task
            if task['label'] == 'Check':
                self.check_task = task
            if task['label'] == 'Run':
                self.run_task = task

    def build(self):
        build_command = self.build_task["command"]+ " " + " ".join(self.build_task["args"])
        return self.container_command(build_command)

    def check(self):
        check_command = self.check_task["command"]+ " " + " ".join(self.check_task["args"])
        return self.container_command(check_command)
    def run(self):
        run_command = self.run_task["command"]+ " " + " ".join(self.run_task["args"])
        return self.container_command(run_command)

    def container_command(self, command):
        return " ".join(["docker", "run","-it","--rm", "-v", self.project_directory+":"+self.contain_project_directory, self.image_name, command])