# ****GPU-Powered Jina AI Flows on GCP VMs: A Practical Guide****

- You could [view the slides online](https://tome.app/pingren/gpu-powered-jina-ai-flows-on-gcp-vms-a-practical-guide-cldcvhcmp15aq6j40jjw8bia7) 

- Below is rough/raw script for the [EAH event](https://www.meetup.com/jina-community-meetup/events/291182236/)
## Intro

Hello everyone, I am a Software Engineer at OpenArt AI. I'm honored speaking to you today about hosting "****GPU-Powered Jina AI Flows on GCP VMs****". 

For those not familiar with OpenArt AI, we are a platform provide millions of AI-generated art pieces and easy-to-use tools to create your own. As you may have noticed, my profile picture on the event poster was generated using AI.(I created it using Photo Booth on OpenArt.) All of the pictures in my slides are also AI-generated. It's just one of the example of the amazing things that can be done by generative AI. If you are interested, feel free to check it out at openart.ai.

Let me talk a few questions about this talk before diving into the topic directly.

### Who would be interested in this guide?

This talk is for developers who have limited or no experience with cloud platforms such as GCP and AWS. I'll provide simple code and cloud infrastructure examples, so don't worry if you've never deployed an AI service before. I'll also share demo code on my Github, so you can easily try it out for yourself. I am still learning GCP and cloud native technolgy. If you are experts and find this talk too easy, please accept my apologies in advance.

### What are benifits to use VM with GPU?

1. It is relatively simple to create and manage Cloud VMs with GPUs, compared to other options.
2. You can quickly test your GPU workflows on a VMwhich allows you to gain instant feedback and make adjustments as needed. This is very useful when you don't have access to a high-performance GPU in your development machine.
3. GCP can assit in scaling up your AI services with just a few clicks. This allows you to take your experiments and quickly turn them into production-ready services.

Now let's dive into the code and demo. Please feel free to ask questions at any time in the chat. 

## Configuring VM and Jina Flows

In this section I will set up the VM and run the service

### Setting up the VM

Let’s go to the Google cloud dashboard for Compute engine. You can get into here by using the search bar. And if you're first time to use this, it may ask you to enable the API and you need to set up a billing account. After fill out billing information, it should will give you some trial credits to play around.

Let’ create a VM by clicking create an instance button here. We will choose a T4 GPU, it is the most affordable GPU option on GCP. We will use the minimum CPU and memory settings. To allow for external HTTP requests, we will configure network tags on the VM.

We will use the Deep Learning VM image to create a new VM, which includes the latest version of PyTorch with CUDA support.

The code is a simple JINA flow for image variations([InstructPix2Pix](https://github.com/timothybrooks/instruct-pix2pix)) in Stable Diffusion, which takes an image URL and a prompt as input and returns its modified version. The code has already been written and pushed to Github. Now, let's get it up and running on a GCP VM.

### Installing the Jina flow

Once the VM has finished booting, we will log in and clone the codebase from Github. After installing the necessary requirements, we will start the flow to ensure it works as expected.

### Keeping the flow running

To keep the flow running even after restarting the VM, we will use PM2. We will install PM2 and set it up to run the flow automatically. Finally, we will reboot the VM to test if PM2 is functioning correctly.

## Logging and Monitoring

Now let’s talking a little bit about logging and monitoring. I will introduce the minimal set up to get basic logging and monioring by lerveragign Cloud Logging API and Ops Agent. Let's set them up.

JINA integrates with OpenTelemetry. We could set up a Collector to collect, store, and visualize the traces and metrics data. The following chart illustrates how it works. The yellow parts in the chart represent the parts that need to be set up.

![chart](https://tome.imgix.net/tomeAssets/cldcvgulo14x11j3vd1mc08zn/assets/cldcvhcmp15aq6j40jjw8bia7/38164313-338c-4690-a529-7428f0fb142f.png?dl=)

## Deployment and Scaling for Production

Now that we have a functional flow running on a single VM. It's time to make it production-ready. To achieve this, we can set up a VM template and an instance group to handle incoming requests.

### Create a VM template

To start, we will shut down the VM and create a disk image, which may take a while, but once complete, we can use it to create a template. The configuration of the template will be similar to the one we used for our VM.

### Create an Instance Group

Second, let’s create the instance group with the template. The instances will automatically scale based on GPU utilization metrics.

### Configure Load Balancer

Finally, we will configure the load balancer with the instance group as the backend. We are required to set up a health checker to ensure the instances is up and running correctly and we set the balancing mode to “utilization” to ensure that the requests are evenly distributed.

With these steps, we have covered all the necessary setup required. Now, we can perform a load test to verify that everything works as expected.

## **Q & A**

Here are some answers to important questions before we conclude.

### How do we upgrade the service?

Upgrading the service is a easy. You simply update the VM and create a new VM template, and then update the instance group with this new template.

For a more efficient and reliable upgrade, I highly recommend automating these steps using scripts and the Google Cloud SDK. This way, you can write and run scripts to perform all the steps, and even perform end-to-end testing on the new template before using it.

### How to reduce GPU cost?

While this guide provides a “production-ready” service, it may not be the most efficient in GPU-intensive scenarios. My suggestion is to design and build your own load balancer, task dispatcher, and scaling metrics to create a more efficient system. For example, instead of measuring GPU metrics, At OpenArt we calculate a Request Computing Score to estimate the workload of different requests with different parameters.

Another solution is to consider using [Spot VM GPU instances](https://cloud.google.com/compute/docs/instances/spot). And don't forget that there are also other providers that offer cheaper GPU options, though there may be trade-offs to consider.

## Thank you

So today we walk through a simple JINA flow on Google Cloud VM, we also set up Google Cloud Loggings and metirics, then we deploy the service into a instance group and make it autosacles based on metrics. I hope you get better understanding of this topic. That’s all for today.