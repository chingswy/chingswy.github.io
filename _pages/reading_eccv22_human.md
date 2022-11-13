---
layout: page
title: ECCV22/human
permalink: /reading_eccv22/
description: 
nav: false
nav_order: 2
years: [2022,]
---


<div class="publications">
<!-- pages/projects.md -->
{%- for y in page.years %}
<h2 class="year">{{y}}</h2>
  {% bibliography -f eccv22_human -q @*[year={{y}}]* %}
{% endfor %}

</div>
