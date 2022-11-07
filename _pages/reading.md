---
layout: page
title: Paper Reading
permalink: /reading/
description: 
nav: true
nav_order: 2
display_categories: [work, fun]
horizontal: false
years: [2022, 2021, 2020]
---

<div class="publications">
<!-- pages/projects.md -->
{%- for y in page.years %}
<h2 class="year">{{y}}</h2>
  {% bibliography -f output -q @*[year={{y}}]* %}
{% endfor %}

</div>