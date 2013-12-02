import json
from db.model_codecs import json_dumps
import pystache


class HtmlRenderer(object):
    template_dirs = ['./html']

    def __init__(self, template_dirs=None):
        self.template_dirs = template_dirs + self.template_dirs
    
    def render_scripts(self, scripts):
        def _render_scripts(scripts):
            _rscripts = []
            for script in scripts:
                rscript = "<script src='%(src)s' " % script
                if 'media' in script:
                    rscript+="media='%(media)s" % script
                rscript+= "></script>"
                _rscripts.append(rscript)
            return "\n".join(_rscripts)
        def add_scripts(text):
            try:
                tscripts = json.loads(text)
                if isinstance(tscripts, list):
                    tscripts.append(scripts)
                return _render_scripts(tscripts)
            except Exception as e:
                return _render_scripts(scripts)
        return add_scripts


    def render(self, template_name, *args, **kwargs):
        if 'scripts' in kwargs:
            kwargs['scripts'] = self.render_scripts(kwargs['scripts'])
        renderer = pystache.Renderer(search_dirs=self.template_dirs)
        return renderer.render_name(template_name, *args, **kwargs).encode()


class JsonRenderer():
    def render(self, **kwargs):
        return json_dumps(kwargs).encode()