from flask.ext.babel import lazy_gettext
from flask.ext.babel import gettext as _gettext
from .security.views import AuthView, ResetPasswordView, UserGeneralView, RoleGeneralView, PermissionViewGeneralView, ViewMenuGeneralView, PermissionGeneralView, IndexView, PermissionView
from .babel.views import LocaleView


class BaseApp():

    lst_baseview = []
    app = None
    static_url_path = '/static/'
    menu = None
    app_name = ""
    languages = None
    _gettext = _gettext

    """
    ------------------------------------
                 INIT
     Add menu with categories inserted
    #-----------------------------------
    """
    def __init__(self, app, menu):
        self.menu = menu
        self.app = app
        self.app_name = app.config['APP_NAME']
        self.app_theme = app.config['APP_THEME']
        self.languages = app.config['LANGUAGES']

        self._add_admin_views()

    def _add_admin_views(self):
        self.add_view_no_menu(IndexView)
        self.add_view_no_menu(LocaleView)
        self.add_view_no_menu(AuthView)
        self.add_view_no_menu(ResetPasswordView)

        self.add_view(UserGeneralView, "List Users"
                                        ,"/users/list","user",
                                        "Security")
        self.add_view(RoleGeneralView, "List Roles","/roles/list","tags","Security")
        self.menu.add_separator("Security")
        self.add_view(PermissionViewGeneralView, "Base Permissions","/permissions/list","lock","Security")
        self.add_view(ViewMenuGeneralView, "Views/Menus","/viewmenus/list","list-alt","Security")
        self.add_view(PermissionGeneralView, "Permission on Views/Menus","/permissionviews/list","lock","Security")

    def add_view(self, baseview, name, href, icon, category):
        print "Registering:", category,".", name, "at", href
        self.menu.add_link(name, href, icon, category)
        if baseview not in self.lst_baseview:
            baseview.baseapp = self
            self.lst_baseview.append(baseview)
            self.register_blueprint(baseview)
            self._add_permission(baseview)

    def add_view_no_menu(self, baseview):
        if baseview not in self.lst_baseview:
            baseview.baseapp = self
            self.lst_baseview.append(baseview)
            self.register_blueprint(baseview)
            self._add_permission(baseview)

    def _add_permission(self, baseview):
        pvm = PermissionView()
        bv = baseview()
        try:
            pvm.add_view_permissions(bv.base_permissions, bv.__class__.__name__)
        except:
            print "General _add_permission Error: DB not created?"
        bv = None
        pvm = None

    def register_blueprint(self, baseview):
        self.app.register_blueprint(baseview().create_blueprint(self))
