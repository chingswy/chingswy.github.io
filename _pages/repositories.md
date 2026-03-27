---
layout: page
permalink: /repositories/
title: repositories
nav: false
nav_order: 3
---

## GitHub users

{% if site.data.repositories.github_users %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.html username=user %}
  {% endfor %}
</div>
{% endif %}

---

## GitHub Repositories

{% if site.data.repositories.github_repos %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for item in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=item.repo stars=item.stars %}
  {% endfor %}
</div>
{% endif %}

## Star History

{% for item in site.data.repositories.github_repos %}
[![Star History Chart](https://api.star-history.com/svg?repos={{item.repo}}&type=Date)](https://star-history.com/#{{item.repo}}&Date)
{% endfor %}
