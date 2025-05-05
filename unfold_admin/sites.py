# from unfold.sites import UnfoldAdminSite


# class CustomUnfoldAdminSite(UnfoldAdminSite):
#     site_header = "Unfold Admin Panel"
#     site_title = "Unfold Admin"
#     index_title = "Добро пожаловать в Unfold админку"


# unfold_admin_site = CustomUnfoldAdminSite(name='unfold_admin')

from unfold.sites import UnfoldAdminSite


class NewUnfoldAdminSite(UnfoldAdminSite):
    pass

# You can route to new admin by "original-name-here-not-admin:index"
new_admin_site = NewUnfoldAdminSite(name="original-name-here-not-admin")
