class Log:
    def __init__(self, name):
        self.title = name
    
    def create_log(self, name, data):
        with open(f'{name}-{self.title}.txt', 'a', encoding='utf8') as file:
            file.write(f'-->{data}\n\n')
