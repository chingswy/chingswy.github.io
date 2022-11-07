---
layout: page
title: Paper Reading
permalink: /reading/
description: 
nav: true
nav_order: 2
display_categories: [work, fun]
tags: ['monocular', 'pose_estimation', 'neural_rendering', 'human', 'human_representation']
horizontal: false
years: [2022, 2021, 2020]
---

<script>
function heredoc(fn) {
  return fn.toString().split('\n').slice(1,-1).join('\n') + '\n'
}
</script>

{% for tag in page.tags -%}
<script>
   function reloadPage_{{tag}}() {
      var inputs = document.getElementsByClassName("publications");
      inputs[0].innerHTML = heredoc(function(){/*
      {% bibliography -f output -q @*[tags~={{tag}}]* %}
      */});
    }
</script>
{% endfor -%}


###### Tags:

{% for tag in page.tags -%}
<a onclick="reloadPage_{{tag}}()"> <i class="fas fa-hashtag fa-sm"></i> {{ tag }}</a> &nbsp;
{% endfor -%}

<div class="publications">
<!-- pages/projects.md -->
{%- for y in page.years %}
<h2 class="year">{{y}}</h2>
  {% bibliography -f output -q @*[year={{y}}]* %}
{% endfor %}

</div>
