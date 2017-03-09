# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def map_and_create_new_ranks(apps, schema_editor):

    Rank = apps.get_model("cnto", "Rank")

    try:
        Rank.objects.get(name__iexact="res")
    except Rank.DoesNotExist:
        res_type = Rank(name="Res")
        res_type.save()

    try:
        ssgt_rank = Rank.objects.get(name__iexact="nco")
        ssgt_rank.name = "SSgt"
        ssgt_rank.save()
    except Rank.DoesNotExist:
        ssgt_rank = Rank(name="SSgt")
        ssgt_rank.save()

    try:
        srnco_rank = Rank.objects.get(name__iexact="srnco")
        jrnco_rank = Rank.objects.get(name__iexact="jrnco")

        Member = apps.get_model("cnto", "Member")

        members = Member.objects.all()
        for member in members:
            if member.rank == srnco_rank or member.rank == jrnco_rank:
                member.rank = ssgt_rank
                member.save()

        srnco_rank.delete()
        jrnco_rank.delete()
    except Rank.DoesNotExist:
        pass


def unmap_ranks(apps, schema_editor):

    Rank = apps.get_model("cnto", "Rank")

    nco_rank = Rank.objects.get(name__iexact="ssgt")
    nco_rank.name = "NCO"
    nco_rank.save()

    srnco_rank = Rank(name="SrNCO")
    srnco_rank.save()
    jrnco_rank = Rank(name="JrNCO")
    jrnco_rank.save()

    Member = apps.get_model("cnto", "Member")

    res_rank = Rank.objects.get(name__iexact="res")
    gnt_rank = Rank.objects.get(name__iexact="gnt")

    members = Member.objects.all()
    for member in members:
        if member.rank == res_rank:
            member.rank = gnt_rank
            member.save()

    res_rank.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0034_absencetype_deprecated'),
    ]

    operations = [
        migrations.RunPython(map_and_create_new_ranks, unmap_ranks),
    ]
