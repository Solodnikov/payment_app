from unfold.sites import UnfoldAdminSite


class NewUnfoldAdminSite(UnfoldAdminSite):
    site_header = "Unfold Admin Panel"
    site_title = "Unfold Admin"
    index_title = "Добро пожаловать в Unfold админку"


unfold_admin_site = NewUnfoldAdminSite(name="unfold_admin")
