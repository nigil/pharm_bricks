from django.contrib.admin.widgets import AdminFileWidget


class AdminImageFieldWidget(AdminFileWidget):
    template_name = 'admin/widgets/image.html'
