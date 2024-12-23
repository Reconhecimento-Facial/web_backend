from fastapi import Form


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
