from keystoneauth1 import loading

from s11auth import plugin


class S11Auth(loading.BaseIdentityLoader):

    @property
    def plugin_class(self):
        return plugin.S11Auth

    def get_options(self):
        options = super(S11Auth, self).get_options()

        options.extend([
            loading.opts.Opt('project-id', help='Project ID to scope to'),
        ])

        options.extend([
            loading.opts.Opt('redirect-port', help='Port to listen on for redirect', default='8080'),
        ])

        return options
