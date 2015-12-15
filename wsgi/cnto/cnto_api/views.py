from django.http.response import JsonResponse
from django.shortcuts import redirect

from cnto.models import Rank, Member, MemberGroup


def chain_of_command_data(request):
    """Return the daily process main overview page.
    """
    officers = {}
    officer_rank_names = ["SrNCO", "NCO", "JrNCO"]

    for officer_rank_name in officer_rank_names:
        officers[officer_rank_name] = []
        for member in Member.objects.all().filter(rank=Rank.objects.filter(name__iexact=officer_rank_name)).order_by("name"):
            officers[officer_rank_name].append(member.name)

    groups = {}
    for group in MemberGroup.objects.all().order_by("name"):
        groups[group.name] = {}
        groups[group.name]["leaders"] = []

        leader_names = []
        if group.leader is not None:
            groups[group.name]["leaders"].append({
                "name": group.leader.name,
                "rank": group.leader.rank.name
            })
            leader_names.append(group.leader.name)

        groups[group.name]["members"] = []
        for member in Member.objects.filter(member_group=group).order_by("name"):
            if member.name in leader_names:
                continue

            groups[group.name]["members"].append({
                "name": member.name,
                "rank": member.rank.name
            })

    result = {
        "officer_ranks": officer_rank_names,
        "officers": officers,
        "groups": groups
    }

    return JsonResponse(result)
