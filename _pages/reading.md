---
layout: page
title: Paper Reading
permalink: /reading/
description: 
nav: false
nav_order: 2
years: [2022, 2021, 2020, 2019, 2018, 2017]
---


<div class="publications">
<!-- pages/projects.md -->
{%- for y in page.years %}
<h2 class="year">{{y}}</h2>
  {% bibliography -f output -q @*[year={{y}}]* %}
{% endfor %}

</div>
