# coding: utf-8
import datetime

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned

from .const import PERSON_TYPE_DECLARATION
from .const import PERSON_TYPE_PERSON


def row_count(cursor, model_name):
    cursor.execute('SELECT COUNT(*) FROM privilege_{}'.format(model_name))
    return cursor.fetchone()[0]


def get_privilege_for_exemption(exemption):
    """Получение или создание privilege по id exemption.

    Учитывается ситуация, когда в таблице присутствуют дубли.
    """

    privilege_model = apps.get_model('privilege.Privilege')
    try:
        privilege, _ = privilege_model.objects.get_or_create(
            exemption_id=exemption
        )
    except MultipleObjectsReturned:
        privilege = privilege_model.objects.filter(
            exemption_id=exemption
        ).order_by('id').first()
    return privilege


def move_personprivilege_data():
    """Перенос льгот физлиц."""

    getprivilegedata_model = apps.get_model('get_privilege.GetPrivilegeData')

    personprivilege_model = apps.get_model('privilege.PersonPrivilege')
    personprivilegeinterval_model = apps.get_model(
        'privilege.PersonPrivilegeInterval'
    )

    privilege_for_exemptions = {}

    for item in getprivilegedata_model.objects.filter(
        person_type=PERSON_TYPE_PERSON
    ).values_list(
        'risid', 'exemption', 'start_date', 'expiration_date',
        'deleted', 'deleted_date',
    ).distinct():
        (risid, exemption, start_date, expiration_date,
         deleted, deleted_date) = item

        privilege = privilege_for_exemptions.get(exemption)
        if not privilege:
            privilege = get_privilege_for_exemption(exemption)
            privilege_for_exemptions[exemption] = privilege

        personprivilege, _ = personprivilege_model.objects.get_or_create(
            person_id=risid,
            privilege=privilege
        )

        # Если существует с таким названием и датой окончания, игнорируем
        if personprivilegeinterval_model.objects.filter(
            owner=personprivilege,
            expiration_date=expiration_date,
            deleted=deleted,
            deleted_date=deleted_date,
        ).exists():
            continue

        # Если существует с таким названием и другой датой окончания,
        # создаем запись о сроке действия.
        # Указываем дату ответа в качестве даты изменения (обновления) записи
        if personprivilegeinterval_model.objects.filter(
            owner=personprivilege
        ).exists():
            personprivilegeinterval_model.objects.update_or_create(
                owner=personprivilege,
                start_date=start_date,
                expiration_date=expiration_date,
                deleted=False,
                defaults={
                    'expiration_date': expiration_date,
                    'deleted': deleted,
                    'deleted_date': deleted_date,
                    'modified': datetime.datetime.now(),
                }
            )

        # Если такой нет, то создаем запись о льготе и запись о сроке действия.
        # Указываем дату получения ответа в качестве даты создания записи.
        else:
            personprivilegeinterval_model.objects.create(
                owner=personprivilege,
                start_date=start_date,
                expiration_date=expiration_date,
                deleted=deleted,
                deleted_date=deleted_date,
            )


def move_declarationprivilege_data():
    """Перенос льгот заявлений."""

    getprivilegedata_model = apps.get_model('get_privilege.GetPrivilegeData')

    declarationprivilege_model = apps.get_model(
        'privilege.DeclarationPrivilege'
    )
    declarationprivilegeinterval_model = apps.get_model(
        'privilege.DeclarationPrivilegeInterval'
    )

    privilege_for_exemptions = {}

    for item in getprivilegedata_model.objects.filter(
        person_type=PERSON_TYPE_DECLARATION
    ).values_list(
        'risid', 'exemption', 'start_date', 'expiration_date',
        'deleted', 'deleted_date',
    ).distinct():
        (risid, exemption, start_date, expiration_date,
         deleted, deleted_date) = item

        privilege = privilege_for_exemptions.get(exemption)
        if not privilege:
            privilege = get_privilege_for_exemption(exemption)
            privilege_for_exemptions[exemption] = privilege

        declarationprivilege, _ = (
            declarationprivilege_model.objects.get_or_create(
                declaration_id=risid,
                privilege=privilege
            )
        )
        # Если существует с таким названием и датой окончания, игнорируем
        if declarationprivilegeinterval_model.objects.filter(
            owner=declarationprivilege,
            expiration_date=expiration_date,
            deleted=deleted,
            deleted_date=deleted_date,
        ).exists():
            continue

        # Если существует с таким названием и другой датой окончания,
        # создаем запись о сроке действия.
        # Указываем дату ответа в качестве даты изменения (обновления) записи
        if declarationprivilegeinterval_model.objects.filter(
            owner=declarationprivilege
        ).exists():
            declarationprivilegeinterval_model.objects.update_or_create(
                owner=declarationprivilege,
                start_date=start_date,
                expiration_date=expiration_date,
                deleted=False,
                defaults={
                    'expiration_date': expiration_date,
                    'deleted': deleted,
                    'deleted_date': deleted_date,
                    'modified': datetime.datetime.now(),
                }
            )

        # Если такой нет, то создаем запись о льготе и запись о сроке действия.
        # Указываем дату получения ответа в качестве даты создания записи.
        else:
            declarationprivilegeinterval_model.objects.create(
                owner=declarationprivilege,
                start_date=start_date,
                expiration_date=expiration_date,
                deleted=deleted,
                deleted_date=deleted_date,
            )
