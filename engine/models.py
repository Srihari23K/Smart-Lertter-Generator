class TemplateModel:
    def __init__(self, name, title, content):
        self.name = name
        self.title = title
        self.content = content
    def __repr__(self):
        return f"<Template {self.name}>"