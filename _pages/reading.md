---
layout: page
title: Paper Reading
permalink: /reading/
description: 
nav: true
nav_order: 2
---


<div class="publications">
<!-- pages/projects.md -->
{%- for y in site.data.reading.years %}
<h2 class="year">{{y}}</h2>
  {% bibliography -f output -q @*[year={{y}}]* %}
{% endfor %}

</div>
