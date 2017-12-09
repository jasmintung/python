from core import role

# FTP Guest类


class Guest(role.RoleBase):

    def __init__(self, user_name, password):
        super(Guest, self).__init__(user_name, password)
