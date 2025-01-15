from datetime import date

from fastapi import Form


def form_body_user_schema_put(cls):
    new_parameters = []
    for arg in cls.__signature__.parameters.values():
        if arg.name == 'id':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        ...,
                        description='User ID',
                    ),
                )
            )
        elif arg.name == 'phone_number':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        default=None,
                        pattern=r'^\(\d{2}\) 9\d{4}-\d{4}$|^$',
                        description='Telefone no formato (DDD) 91234-5678',
                    )
                )
            )
        elif arg.name == 'cpf':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        default=None,
                        pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^$',
                        description='CPF no formato XXX.XXX.XXX-XX',
                    ),
                )
            )
        elif arg.name == 'email':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        default='default@default.com',
                    ),
                )
            )
        elif arg.name == 'date_of_birth':
            new_parameters.append(arg.replace(default=Form(default=date.min)))
        elif arg.name == 'status':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        default=None,
                        description="'active', 'inactive' or empty ''",
                    )
                )
            )
        else:
            new_parameters.append(arg.replace(default=Form(default=None)))
    cls.__signature__ = cls.__signature__.replace(parameters=new_parameters)
    return cls


def form_body_user_schema(cls):
    new_parameters = []
    for arg in cls.__signature__.parameters.values():
        if arg.name == 'phone_number':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        ...,
                        pattern=r'^\(\d{2}\) 9\d{4}-\d{4}$',
                        description='Telefone no formato (DDD) 91234-5678',
                    )
                )
            )
        elif arg.name == 'cpf':
            new_parameters.append(
                arg.replace(
                    default=Form(
                        ...,
                        pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                        description='CPF no formato XXX.XXX.XXX-XX',
                    )
                )
            )
        else:
            new_parameters.append(arg.replace(default=Form(...)))
    cls.__signature__ = cls.__signature__.replace(parameters=new_parameters)
    return cls


def form_body_environment_schema(cls):
    new_parameters = []
    for arg in cls.__signature__.parameters.values():
        new_parameters.append(arg.replace(default=Form(...)))
    cls.__signature__ = cls.__signature__.replace(parameters=new_parameters)
    return cls
