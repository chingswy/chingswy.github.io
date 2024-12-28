---
layout: about
title: about
permalink: /
# subtitle: <a href='#'>Affiliations</a>. Address. Contacts. Moto. Etc.

profile:
  align: right
  address: "https://sketchfab.com/models/b0fb28cf0fed4a1d8a696b5152ca775c/embed"
  # image: prof_pic.jpg
  # image_circular: false # crops the image to make it circular
  # address: >
  #   <p>555 your office number</p>
  #   <p>123 your address street</p>
  #   <p>Your City, State 12345</p>

news: false  # includes a list of news items
selected_papers: true # includes a list of papers marked as "selected={true}"
years: [2024, 2023, 2022, 2021, 2020]
social: true  # includes social icons at the bottom of the page
---

I am currently working at Tencent (2024.7-), where my focus is on human motion capture and generation under multimodal inputs. Prior to this, I was a Ph.D. student in Computer Science at [Zhejiang University](http://www.zju.edu.cn/english/) from 2019 to 2024, under the supervision of [Xiaowei Zhou](http://xzhou.me). My research interests lie at the intersection of computer vision and computer graphics, with a particular emphasis on 3D human pose estimation and generation, 3D reconstruction, and novel view synthesis.

During my past career, my main focus was on the [EasyMoCap](https://github.com/zju3dv/EasyMocap/) repository. The goal of this repository is to **make human motion capture more accessible and straightforward**. It encompasses a collection of code from my work over the past few years and includes essential tools for the field of human motion capture, such as camera calibration, interactive keypoint annotation, visualization, and more.

<div class="repositories" align="center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=repo %}
  {% endfor %}
</div>

## Demos

#### Professional Motion Capture with Multi-Camera Systems

<div class="row">
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/mocap/02_fitsmpl_output.mp4" position="left" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/mocap/04_ballet.mp4" position="right"  %}
    </div>
</div>

#### Simple Motion Capture from Complex Internet Videos

<div class="row">
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/mocap/1v1p-test-yusheng.mp4" position="left"%}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/mocap/1v1p-test-cxk.mp4" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/mocap/03_fitmono_mano.mp4" position="right"  %}
    </div>
</div>

#### Novel View Synthesis

<div class="row">
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_soccer1-6.mp4" position="left" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_soccer1-beijia.mp4" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_soccer1-yuang.mp4" position="right"  %}
    </div>
</div>

#### 4D Scene Reconstruction and Editing

<div class="row">
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_boxing2.mp4" position="left" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_basketball_disappear.mp4" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_handstand.mp4" %}
    </div>
    <div class="col-sm mt-0 mt-md-0">
        {% include video.html path="assets/multinb/demo_juggle.mp4" position="right" %}
    </div>
</div>

