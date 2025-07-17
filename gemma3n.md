https://ai.google.dev/gemma/docs/gemma-3n

Gemma 3n released with audio input and optimized for use in everyday devices! Learn more
Home
Gemma
Models
Docs
Was this helpful?

Send feedbackGemma 3n model overview


Gemma 3n is a generative AI model optimized for use in everyday devices, such as phones, laptops, and tablets. This model includes innovations in parameter-efficient processing, including Per-Layer Embedding (PLE) parameter caching and a MatFormer model architecture that provides the flexibility to reduce compute and memory requirements. These models feature audio input handling, as well as text and visual data.

Gemma 3n includes the following key features:

Audio input: Process sound data for speech recognition, translation, and audio data analysis. Learn more
Visual and text input: Multimodal capabilities let you handle vision, sound, and text to help you understand and analyze the world around you. Learn more
Vision encoder: High-performance MobileNet-V5 encoder substantially improves speed and accuracy of processing visual data. Learn more
PLE caching: Per-Layer Embedding (PLE) parameters contained in these models can be cached to fast, local storage to reduce model memory run costs. Learn more
MatFormer architecture: Matryoshka Transformer architecture allows for selective activation of the models parameters per request to reduce compute cost and response times. Learn more
Conditional parameter loading: Bypass loading of vision and audio parameters in the model to reduce the total number of loaded parameters and save memory resources. Learn more
Wide language support: Wide linguistic capabilities, trained in over 140 languages.
32K token context: Substantial input context for analyzing data and handling processing tasks.
Try Gemma 3n Get it on Kaggle Get it on Hugging Face

As with other Gemma models, Gemma 3n is provided with open weights and licensed for responsible commercial use, allowing you to tune and deploy it in your own projects and applications.

Tip: If you are interested in building generative AI solutions for Android mobile applications, check out Gemini Nano. For more information, see the Android Gemini Nano developer docs.
Model parameters and effective parameters
Gemma 3n models are listed with parameter counts, such as E2B and E4B, that are lower than the total number of parameters contained in the models. The E prefix indicates these models can operate with a reduced set of Effective parameters. This reduced parameter operation can be achieved using the flexible parameter technology built into Gemma 3n models to help them run efficiently on lower resource devices.

The parameters in Gemma 3n models are divided into 4 main groups: text, visual, audio, and per-layer embedding (PLE) parameters. With standard execution of the E2B model, over 5 billion parameters are loaded when executing the model. However, using parameter skipping and PLE caching techniques, this model can be operated with an effective memory load of just under 2 billion (1.91B) parameters, as illustrated in Figure 1.

Gemma 3n diagram of parameter usage

Figure 1. Gemma 3n E2B model parameters running in standard execution versus an effectively lower parameter load using PLE caching and parameter skipping techniques.

Using these parameter offloading and selective activation techniques, you can run the model with a very lean set of parameters or activate additional parameters to handle other data types such as visual and audio. These features enable you to ramp up model functionality or ramp down capabilities based on device capabilities or task requirements. The following sections explain more about the parameter efficient techniques available in Gemma 3n models.

PLE caching
Gemma 3n models include Per-Layer Embedding (PLE) parameters that are used during model execution to create data that enhances the performance of each model layer. The PLE data can be generated separately, outside the operating memory of the model, cached to fast storage, and then added to the model inference process as each layer runs. This approach allows PLE parameters to be kept out of the model memory space, reducing resource consumption while still improving model response quality.

MatFormer architecture
Gemma 3n models use a Matryoshka Transformer or MatFormer model architecture that contains nested, smaller models within a single, larger model. The nested sub-models can be used for inferences without activating the parameters of the enclosing models when responding to requests. This ability to run just the smaller, core models within a MatFormer model can reduce compute cost, and response time, and energy footprint for the model. In the case of Gemma 3n, the E4B model contains the parameters of the E2B model. This architecture also lets you select parameters and assemble models in intermediate sizes between 2B and 4B. For more details on this approach, see the MatFormer research paper. Try using MatFormer techniques to reduce the size of a Gemma 3n model with the MatFormer Lab guide.

Conditional parameter loading
Similar to PLE parameters, you can skip loading of some parameters into memory, such as audio or visual parameters, in the Gemma 3n model to reduce memory load. These parameters can be dynamically loaded at runtime if the device has the required resources. Overall, parameter skipping can further reduce the required operating memory for a Gemma 3n model, enabling execution on a wider range of devices and allowing developers to increase resource efficiency for less demanding tasks.


Ready to start building? Get started with Gemma models!

Was this helpful?

Send feedback
Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-06-30 UTC.




google
/
gemma-3n-E4B-it-litert-preview 

like
1.33k

Follow

Google
19k
Image-Text-to-Text

arxiv:
17 papers

License:
gemma
Model card
Files and versions
xet
Community
45
Gated model
You have been granted access to this model

This repository corresponds to the Preview version of Gemma 3n E2B, to be used with Google AI Edge. You can also try it out in Google AI Studio.

The current checkpoint only supports text and vision input. We are actively working to roll out full multimodal features and are collaborating with open-source partners to bring Gemma 3n to the open-source community in the coming weeks.

Gemma 3n models have a novel architecture that allows them to run with a smaller number of effective parameters. They also have a Matformer architecture that allows nesting multiple models. Learn more about these techniques in the Gemma documentation.

Gemma 3n model card
Model Page: Gemma 3n

Resources and Technical Documentation:

Responsible Generative AI Toolkit
Gemma on Kaggle
Google AI Edge documentation to run on mobile
Try on Android by downloading our Google AI Edge Gallery sample app
Terms of Use: Terms
Authors: Google DeepMind

Model Information
Summary description and brief definition of inputs and outputs.

Description
Gemma is a family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models. Gemma models are well-suited for a variety of content understanding tasks, including question answering, summarization, and reasoning. Their relatively small size makes it possible to deploy them in environments with limited resources such as laptops, desktops or your own cloud infrastructure, democratizing access to state of the art AI models and helping foster innovation for everyone.

Gemma 3n models are designed for efficient execution on low-resource devices. They are capable of multimodal input, handling text, image, video, and audio input, and generating text outputs, with open weights for instruction-tuned variants. These models were trained with data in over 140 spoken languages.

Gemma 3n models use selective parameter activation technology to reduce resource requirements. This technique allows the models to operate at an effective size of 2B and 4B parameters, which is lower than the total number of parameters they contain. For more information on Gemma 3n's efficient parameter management technology, see the Gemma 3n page.

Inputs and outputs
Input:
Text string, such as a question, a prompt, or a document to be summarized
Images, normalized to 256x256, 512x512, or 768x768 resolution and encoded to 256 tokens each
Audio data encoded to 6.25 tokens per second from a single channel
Total input context of 32K tokens
Output:
Generated text in response to the input, such as an answer to a question, analysis of image content, or a summary of a document
Total output length up to 32K tokens, subtracting the request input tokens
Citation
@article{gemma_3n_2025,
    title={Gemma 3n},
    url={https://ai.google.dev/gemma/docs/gemma-3n},
    publisher={Google DeepMind},
    author={Gemma Team},
    year={2025}
}

Model Data
Data used for model training and how the data was processed.

Training Dataset
These models were trained on a dataset that includes a wide variety of sources totalling approximately 11 trillion tokens. The knowledge cutoff date for the training data was June 2024. Here are the key components:

Web Documents: A diverse collection of web text ensures the model is exposed to a broad range of linguistic styles, topics, and vocabulary. The training dataset includes content in over 140 languages.
Code: Exposing the model to code helps it to learn the syntax and patterns of programming languages, which improves its ability to generate code and understand code-related questions.
Mathematics: Training on mathematical text helps the model learn logical reasoning, symbolic representation, and to address mathematical queries.
Images: A wide range of images enables the model to perform image analysis and visual data extraction tasks.
Audio: A diverse set of sound samples enables the model to recognize speech, transcribe text from recordings, and identify information in audio data.
The combination of these diverse data sources is crucial for training a powerful multimodal model that can handle a wide variety of different tasks and data formats.

Data Preprocessing
Here are the key data cleaning and filtering methods applied to the training data:

CSAM Filtering: Rigorous CSAM (Child Sexual Abuse Material) filtering was applied at multiple stages in the data preparation process to ensure the exclusion of harmful and illegal content.
Sensitive Data Filtering: As part of making Gemma pre-trained models safe and reliable, automated techniques were used to filter out certain personal information and other sensitive data from training sets.
Additional methods: Filtering based on content quality and safety in line with our policies.
Implementation Information
Details about the model internals.

Hardware
Gemma was trained using Tensor Processing Unit (TPU) hardware (TPUv4p, TPUv5p and TPUv5e). Training generative models requires significant computational power. TPUs, designed specifically for matrix operations common in machine learning, offer several advantages in this domain:

Performance: TPUs are specifically designed to handle the massive computations involved in training generative models. They can speed up training considerably compared to CPUs.
Memory: TPUs often come with large amounts of high-bandwidth memory, allowing for the handling of large models and batch sizes during training. This can lead to better model quality.
Scalability: TPU Pods (large clusters of TPUs) provide a scalable solution for handling the growing complexity of large foundation models. You can distribute training across multiple TPU devices for faster and more efficient processing.
Cost-effectiveness: In many scenarios, TPUs can provide a more cost-effective solution for training large models compared to CPU-based infrastructure, especially when considering the time and resources saved due to faster training.
These advantages are aligned with Google's commitments to operate sustainably.

Software
Training was done using JAX and ML Pathways. JAX allows researchers to take advantage of the latest generation of hardware, including TPUs, for faster and more efficient training of large models. ML Pathways is Google's latest effort to build artificially intelligent systems capable of generalizing across multiple tasks. This is specially suitable for foundation models, including large language models like these ones.

Together, JAX and ML Pathways are used as described in the paper about the Gemini family of models: "the 'single controller' programming model of Jax and Pathways allows a single Python process to orchestrate the entire training run, dramatically simplifying the development workflow."

Evaluation
Model evaluation metrics and results.

Benchmark Results
These models were evaluated at full precision (float32) against a large collection of different datasets and metrics to cover different aspects of content generation. Evaluation results marked with IT are for instruction-tuned models. Evaluation results marked with PT are for pre-trained models.

Reasoning and factuality
Benchmark	Metric	n-shot	E2B PT	E4B PT
HellaSwag	Accuracy	10-shot	72.2	78.6
BoolQ	Accuracy	0-shot	76.4	81.6
PIQA	Accuracy	0-shot	78.9	81.0
SocialIQA	Accuracy	0-shot	48.8	50.0
TriviaQA	Accuracy	5-shot	60.8	70.2
Natural Questions	Accuracy	5-shot	15.5	20.9
ARC-c	Accuracy	25-shot	51.7	61.6
ARC-e	Accuracy	0-shot	75.8	81.6
WinoGrande	Accuracy	5-shot	66.8	71.7
BIG-Bench Hard	Accuracy	few-shot	44.3	52.9
DROP	Token F1 score	1-shot	53.9	60.8
Multilingual
Benchmark	Metric	n-shot	E2B IT	E4B IT
MGSM	Accuracy	0-shot	53.1	60.7
WMT24++ (ChrF)	Character-level F-score	0-shot	42.7	50.1
Include	Accuracy	0-shot	38.6	57.2
MMLU (ProX)	Accuracy	0-shot	8.1	19.9
OpenAI MMLU	Accuracy	0-shot	22.3	35.6
Global-MMLU	Accuracy	0-shot	55.1	60.3
ECLeKTic	ECLeKTic score	0-shot	2.5	1.9
STEM and code
Benchmark	Metric	n-shot	E2B IT	E4B IT
GPQA Diamond	RelaxedAccuracy/accuracy	0-shot	24.8	23.7
LiveCodeBench v5	pass@1	0-shot	18.6	25.7
Codegolf v2.2	pass@1	0-shot	11.0	16.8
AIME 2025	Accuracy	0-shot	6.7	11.6
Additional benchmarks
Benchmark	Metric	n-shot	E2B IT	E4B IT
MMLU	Accuracy	0-shot	60.1	64.9
MBPP	pass@1	3-shot	56.6	63.6
HumanEval	pass@1	0-shot	66.5	75.0
LiveCodeBench	pass@1	0-shot	13.2	13.2
HiddenMath	Accuracy	0-shot	27.7	37.7
Global-MMLU-Lite	Accuracy	0-shot	59.0	64.5
MMLU (Pro)	Accuracy	0-shot	40.5	50.6
Android Performance Benchmarks with Google AI Edge
Note that all benchmark stats are from a Samsung S25 Ultra with 4096 KV cache size, 1024 tokens prefill, 256 tokens decode.

These numbers will continue to improve while Gemma 3n is in preview.

Weight Quantization	Backend	Prefill (tokens/sec)	Decode (tokens/sec)	Time to first token (sec)	Model size (MB)	Peak RSS Memory (MB)	GPU Memory (MB)
dynamic_int4	CPU	118	12.8	9.2	4201	3924	193
dynamic_int4	GPU	446	16.1	15.1	4201	5504	3048
Model size: measured by the size of the .tflite flatbuffer (serialization format for LiteRT models)
The inference on CPU is accelerated via the LiteRT XNNPACK delegate with 4 threads
Benchmark on CPU is done assuming XNNPACK cache is enabled
Benchmark on GPU is done assuming model is cached
Vision encoder is always run on GPU with 512x512 resolution
Cpufreq governor is set to performance during benchmark. Observed performance may vary depending on your phone’s hardware and current activity level.
dynamic_int4: quantized model with int4 weights and float activations.
Ethics and Safety
Ethics and safety evaluation approach and results.

Evaluation Approach
Our evaluation methods include structured evaluations and internal red-teaming testing of relevant content policies. Red-teaming was conducted by a number of different teams, each with different goals and human evaluation metrics. These models were evaluated against a number of different categories relevant to ethics and safety, including:

Child Safety: Evaluation of text-to-text and image to text prompts covering child safety policies, including child sexual abuse and exploitation.
Content Safety: Evaluation of text-to-text and image to text prompts covering safety policies including, harassment, violence and gore, and hate speech.
Representational Harms: Evaluation of text-to-text and image to text prompts covering safety policies including bias, stereotyping, and harmful associations or inaccuracies.
In addition to development level evaluations, we conduct "assurance evaluations" which are our 'arms-length' internal evaluations for responsibility governance decision making. They are conducted separately from the model development team, to inform decision making about release. High level findings are fed back to the model team, but prompt sets are held-out to prevent overfitting and preserve the results' ability to inform decision making. Notable assurance evaluation results are reported to our Responsibility & Safety Council as part of release review.

Evaluation Results
For all areas of safety testing, we saw safe levels of performance across the categories of child safety, content safety, and representational harms relative to previous Gemma models. All testing was conducted without safety filters to evaluate the model capabilities and behaviors. For text-to-text, image-to-text, and audio-to-text, and across all model sizes, the model produced minimal policy violations, and showed significant improvements over previous Gemma models' performance with respect to high severity violations. A limitation of our evaluations was they included primarily English language prompts.

Usage and Limitations
These models have certain limitations that users should be aware of.

Intended Usage
Open generative models have a wide range of applications across various industries and domains. The following list of potential uses is not comprehensive. The purpose of this list is to provide contextual information about the possible use-cases that the model creators considered as part of model training and development.

Content Creation and Communication
Text Generation: Generate creative text formats such as poems, scripts, code, marketing copy, and email drafts.
Chatbots and Conversational AI: Power conversational interfaces for customer service, virtual assistants, or interactive applications.
Text Summarization: Generate concise summaries of a text corpus, research papers, or reports.
Image Data Extraction: Extract, interpret, and summarize visual data for text communications.
Audio Data Extraction: Transcribe spoken language, speech translated to text in other languages, and analyze sound-based data.
Research and Education
Natural Language Processing (NLP) and generative model Research: These models can serve as a foundation for researchers to experiment with generative models and NLP techniques, develop algorithms, and contribute to the advancement of the field.
Language Learning Tools: Support interactive language learning experiences, aiding in grammar correction or providing writing practice.
Knowledge Exploration: Assist researchers in exploring large bodies of data by generating summaries or answering questions about specific topics.
Limitations
Training Data
The quality and diversity of the training data significantly influence the model's capabilities. Biases or gaps in the training data can lead to limitations in the model's responses.
The scope of the training dataset determines the subject areas the model can handle effectively.
Context and Task Complexity
Models are better at tasks that can be framed with clear prompts and instructions. Open-ended or highly complex tasks might be challenging.
A model's performance can be influenced by the amount of context provided (longer context generally leads to better outputs, up to a certain point).
Language Ambiguity and Nuance
Natural language is inherently complex. Models might struggle to grasp subtle nuances, sarcasm, or figurative language.
Factual Accuracy
Models generate responses based on information they learned from their training datasets, but they are not knowledge bases. They may generate incorrect or outdated factual statements.
Common Sense
Models rely on statistical patterns in language. They might lack the ability to apply common sense reasoning in certain situations.
Ethical Considerations and Risks
The development of generative models raises several ethical concerns. In creating an open model, we have carefully considered the following:

Bias and Fairness
Generative models trained on large-scale, real-world text and image data can reflect socio-cultural biases embedded in the training material. These models underwent careful scrutiny, input data pre-processing described and posterior evaluations reported in this card.
Misinformation and Misuse
Generative models can be misused to generate text that is false, misleading, or harmful.
Guidelines are provided for responsible use with the model, see the Responsible Generative AI Toolkit.
Transparency and Accountability:
This model card summarizes details on the models' architecture, capabilities, limitations, and evaluation processes.
A responsibly developed open model offers the opportunity to share innovation by making generative model technology accessible to developers and researchers across the AI ecosystem.
Risks identified and mitigations:

Perpetuation of biases: It's encouraged to perform continuous monitoring (using evaluation metrics, human review) and the exploration of de-biasing techniques during model training, fine-tuning, and other use cases.
Generation of harmful content: Mechanisms and guidelines for content safety are essential. Developers are encouraged to exercise caution and implement appropriate content safety safeguards based on their specific product policies and application use cases.
Misuse for malicious purposes: Technical limitations and developer and end-user education can help mitigate against malicious applications of generative models. Educational resources and reporting mechanisms for users to flag misuse are provided. Prohibited uses of Gemma models are outlined in the Gemma Prohibited Use Policy.
Privacy violations: Models were trained on data filtered for removal of certain personal information and other sensitive data. Developers are encouraged to adhere to privacy regulations with privacy-preserving techniques.
Benefits
At the time of release, this family of models provides high-performance open generative model implementations designed from the ground up for responsible AI development compared to similarly sized models.

Using the benchmark evaluation metrics described in this document, these models have shown to provide superior performance to other, comparably-sized open model alternatives.

Downloads last month
-

Downloads are not tracked for this model.
How to track
Inference Providers
NEW
Image-Text-to-Text
This model isn't deployed by any Inference Provider.
🙋
190
Ask for provider support
Model tree for
google/gemma-3n-E4B-it-litert-preview
Adapters
2 models
Finetunes
12 models
Merges
2 models
