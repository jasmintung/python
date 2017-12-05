from core import role

# FTP Real用户类


class Real(role.RoleBase):

    def __init__(self, user_name, password):
        super(Real, self).__init__(user_name, password)

