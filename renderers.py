import pystache


class HtmlRenderer(object):
    template_dirs = ['./html']

    def __init__(self, template_dirs=None):
        self.template_dirs = template_dirs + self.template_dirs

    def render(self, template_name, *args, **kwargs):
        renderer = pystache.Renderer(search_dirs=self.template_dirs)
        return renderer.render_name(template_name, *args, **kwargs).encode()
