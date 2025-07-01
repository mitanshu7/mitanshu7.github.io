---
title: "PaperMatch Analysis"
description: "Exploring how vector embeddings reveal insights about scientific research on arXiv. From distance metrics and vector DB performance to category shifts and dimensionality reduction using PCA, UMAP, and MRL on millions of abstracts."
---

## What do the vectors tell us?

**Mitanshu Sukhwani** • _11 June 2025_

![[**3D Map of arXiv**](../image/arxiv_3d_map_all_years.html)](../image/3d_umap_binary_all.webp)

This post is heavily inspired by this blog post, [Exploring Hacker News by mapping and analyzing 40 million posts and comments for fun](http://web.archive.org/web/20250324014115/https://blog.wilsonl.in/hackerverse/), by [Wilson Lin](http://web.archive.org/web/20240805173635/https://blog.wilsonl.in/).

In [Behind PaperMatch](Behind_PaperMatch.html), we saw a brief overview of how to spin up a semantic search engine and in [Behind PaperMatchBio](Behind_PaperMatchBio.html) we learned about some hacks that go into scraping when you are low on resources. But what about the data that these engines leave behind? Can we study something deeper about the research that we do and how it evolves? Here is my attempt at it.

# Validation

My open-source model of choice, [mixedbread-ai/mxbai-embed-large-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1), was fairing at top spots on [Massive Text Embedding Benchmark (MTEB)](https://huggingface.co/spaces/mteb/leaderboard) leaderboard during the inception of [PaperMatch](https://papermatch.me/) (March 2024). It's a small, only 335 million parameters, embedding model compared to [newer](https://huggingface.co/Qwen/Qwen3-Embedding-8B) [models](https://huggingface.co/Salesforce/SFR-Embedding-2_R) with [billions](https://huggingface.co/GritLM/GritLM-8x7B) of [parameters](https://huggingface.co/nvidia/NV-Embed-v2).

What do small models struggle with? Long [context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows). `mxbai-embed-large-v1` only has a length of $512$ tokens. But how long are all the abstracts on arXiv anyway?

![Histogram of token lengths](../image/papermatch_token_count_distribution.webp)

On first look, bingo! most of the abstracts are covered by the model's context window. But how many are actually out of context? Enjoy some stats below.

```yaml
Total number of papers (as of June 2025): 2754926

Number of papers with token count > 512: 15548
Number of papers with token count <= 512: 2739378

Percentage of papers with token count > 512: 0.56%
Percentage of papers with token count <= 512: 99.44%

Minimum token count: 2
Average token count: 207.62
Maximum token count: 1595
```

Papers with the shortest abstract length:

1. [**Are theoretical results 'Results'?**](https://arxiv.org/abs/1807.11336)

   > **Raymond E. Goldstein** | _July 2018_

   Yes.

2. [**Is AmI (Attacks Meet Interpretability) Robust to Adversarial Examples?**](https://arxiv.org/abs/1902.02322)

   > **Nicholas Carlini** | _February 2019_

   No.

Paper with the longest abstract length:

1. [**On the generation of Arveson weakly continuous semigroups**](https://arxiv.org/abs/1709.05218)

   > **Jean Esterle** (IMB) | _September 2017_

   We consider here one-parameter semigroups

   ...

   we indeed have $F(-A_T)=A_T.$

Phew, model migrations are a pain.

[**Vector Databases Are the Wrong Abstraction**](https://www.timescale.com/blog/vector-databases-are-the-wrong-abstraction) has some good insights!

# Performance

## Distance Metric

Then I wanted to check and turn all the knobs I had. When you are talking about semantic search, there are many metrics with which you can define the "distance" between two vectors.

The most common one is [Euclidean](https://en.wikipedia.org/wiki/Euclidean_distance). Imagine two points on a plane with coordinates $A := (x_1, y_1)$, and $B := (x_2, y_2)$. The square of distance between $A$ and $B$ is:
$$ d(A,B)^2 = (y_2 - y_1 )^2 + (x_2 - x_1)^2 $$
Euclidean distance signifies how close (or far) two points are. Smaller the distance, closer the points, and hence more related they are.

However, when talking about semantic search, the most used metric is [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

![Cosine similarity formula](https://wikimedia.org/api/rest_v1/media/math/render/svg/15d11df2d48da4787ee86a4b8c14551fbf0bc96a)

Cosine similarity ranges from $-1 \to 1$. Where $-1$ tells you that the vectors in question are facing opposite to each other, $0$ tells you orthogonal vector and $1$ tells you both the vectors are facing in the same direction. Embedding models also capture semantic meaning in terms of the direction. And hence, if two vectors are pointing in the same direction, they tend to mean similar things.

![Cosine similarity graph](https://miro.medium.com/v2/resize:fit:824/1*GK56xmDIWtNQAD_jnBIt2g.png)

Another such metric is [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance). It exists for binary vectors, values of which are either $0$ or $1$. Hamming distance is defined by taking bitwise [XOR](https://en.wikipedia.org/wiki/Exclusive_or) of two binary vectors and then summing up the values in resulting vector.

![Hamming distance calulation](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/img/hamming_similarity2.png)

Fun fact, [POPCNT](https://en.wikipedia.org/wiki/SSE4#POPCNT_and_LZCNT) - counts the number of 1 bits, is actually [The NSA Instruction](https://vaibhavsagar.com/blog/2019/09/08/popcount/).

## Index used by the Vector Database

[Milvus](https://milvus.io/) offers a range of distance [metrics](https://milvus.io/docs/metric.md) and vector [indices](https://milvus.io/docs/index.md). We'll compare FLAT and IVF_FLAT.

FLAT is a very simple index. It simply calculates the distance between the query vector and all the vectors in your database. This simplicity comes with the cost of having to compute a lot.

Inverted File FLAT (IVF-FLAT) allows for approximate nearest neighbour search. First you partition your embedding database, then calculate centroids of all the partitions.

![Partition](https://assets.zilliz.com/centroid_09ce775136.png)

Then, when a query vector comes, first you only query the centroids and when you find the closest centroid, you use FLAT search for all the vectors belonging to that cluster.

![IVF-FLAT search](https://assets.zilliz.com/centroid_1_64417f3d6d.png)

Source: [How to Pick a Vector Index in Your Milvus Instance: A Visual Guide](https://zilliz.com/learn/how-to-pick-a-vector-index-in-milvus-visual-guide).

One last thing we need to know about is how the search in [PaperMatch](https://papermatch.me/) works. The following flowchart should make it clear.

![How queries are handled in PaperMatch.](../image/papermatch_flowchart.webp)

Armed with the above parameters, I tried to estimate how they affect the latency of the vector database.

![Latency vs Search limit](../image/papermatch_performance.webp)

We get the best **quality** when we use `COSINE` similarity, `Float32` vectors, along with a `FLAT` index, and **fastest** results on `HAMMING` distance, `Binary` vectors, and `IVF_FLAT` index. Naturally, [PaperMatch](https://papermatch.me/) uses the latter.

But how much quality degradation do we really see? Well, not much since **the top ten results of both the variants are the same**. And assuming most people do not look beyond the top 10 results when then top ones weren't worthwhile in the first place, this works out very well for user experience (UX).

# What about the direction of science itself?

## Category

arXiv started in $1991$ with only about $300$ physics papers in its repo. Now it is one of the biggest preprint repositories hosting close to $3$ million articles and growing at an average rate of about $4.5K$ papers/week. How have the subjects evolved?

![2001 Categories Histogram](../image/2001_category_distribution.webp)

![2011 Categories Histogram](../image/2011_category_distribution.webp)

![2021 Categories Histogram](../image/2021_category_distribution.webp)

![2025 Categories Histogram](../image/2025_category_distribution.webp)

Now you know why arXiv has so many [CS](https://arxiv.org/archive/cs) papers. They account for almost half of a year's worth!

## Dimensionality reduction

### PCA

[Principal Component Analysis](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html), is a statistical technique used to reduce the dimensionality of data (from a vector of size $1024$ to say $2$) by identifying the most important features (principal components) that capture the most variance in a dataset.

![PCA in action](https://numxl.com/wp-content/uploads/principal-component-analysis-pca-featured.png)

We can apply pca to float and binary vectors to see the impact of conversion.

### Float

![Scatter plot PCA of float embeddings, 2011](../image/2011_scatter_float_pca.webp)

![Scatter plot PCA of float embeddings, 2021](../image/2021_scatter_float_pca.webp)

![Scatter plot PCA of float embeddings, 2025](../image/2025_scatter_float_pca.webp)

### Binary

![Scatter plot PCA of binary embeddings, 2011](../image/2011_scatter_binary_pca.webp)

![Scatter plot PCA of binary embeddings, 2021](../image/2021_scatter_binary_pca.webp)

![Scatter plot PCA of binary embeddings, 2025](../image/2025_scatter_binary_pca.webp)

So that is why we get very good results in binary too!

However, there is another technique which gets itself a good name owing to it quality of reductions.

## UMAP

[Uniform Manifold Approximation and Projection](https://umap-learn.readthedocs.io/en/latest/) is a novel manifold learning technique for dimension reduction.

### Float, Euclidean

![Scatter plot UMAP of float embeddings, 2011](../image/2011_scatter_float_umap.webp)

![Scatter plot UMAP of float embeddings, 2021](../image/2021_scatter_float_umap.webp)

![Scatter plot UMAP of float embeddings, 2025](../image/2025_scatter_float_umap.webp)

### Binary, Hamming

![Scatter plot UMAP of binary embeddings, 2011](../image/2011_scatter_binary_umap.webp)

![Scatter plot UMAP of binary embeddings, 2021](../image/2021_scatter_binary_umap.webp)

![Scatter plot UMAP of binary embeddings, 2025](../image/2025_scatter_binary_umap.webp)

UMAP seems to giving much better seperation between subjects. It is quite interesting to see the "**island**" coming up for the year 2025. The "**island**" originally appears in 2024. It can be seen even when we use `cosine` distance.

Bonus! [Mixedbread](https://www.mixedbread.com/) makes the case for their model in the blog post: [64 bytes per embedding, yee-haw 🤠](https://www.mixedbread.com/blog/binary-mrl). Their embedding models is compatible with [Matryoshka Representation Learning (MRL)](https://arxiv.org/abs/2205.13147) and [Vector Quantization](https://www.huggingface.co/blog/embedding-quantization). Essentially, the vectors still hold strong when you convert `float32` to `binary` ($1$ if they are greater than $0$ and to $0$ if they are not) and then chop the vectors in half ($1024 \to 512$) or so.

## MRL

We simply take the first two elements of the embedded vectors directly.

### Float

![Scatter plot MRL of float embeddings, 2011](../image/2011_scatter_float_mrl.webp)

![Scatter plot MRL of float embeddings, 2021](../image/2021_scatter_float_mrl.webp)

![Scatter plot MRL of float embeddings, 2025](../image/2025_scatter_float_mrl.webp)

### Binary

![Scatter plot MRL of binary embeddings, 2011](../image/2011_scatter_binary_mrl.webp)

![Scatter plot MRL of binary embeddings, 2021](../image/2021_scatter_binary_mrl.webp)

![Scatter plot MRL of binary embeddings, 2025](../image/2025_scatter_binary_mrl.webp)

Float seems to performs quite well, but the binary one conveys no information whatsoever.

# [**3D Map of arXiv**](../image/arxiv_3d_map_all_years.html)

For fun, I also performed `UMAP` for _all of arXiv_ on the `Binary` vectors using `Hamming` distance as metric. Peak memory usage reached 165 GB of RAM on `AMD EPYC 8434P` 48-Core Processor running `Ubuntu Server`. `Float` with `Cosine` exceeded the RAM+SWAP (256 + 200 GB) and hence could not be performed.

Please explore it at: [**3D Map of arXiv**](../image/arxiv_3d_map_all_years.html). Note that the number of points (papers) displayed are sampled to 1,00,000 for performance reasons.

The source code & the data for the analysis is available at [mitanshu7/PaperMatch_Analysis](https://github.com/mitanshu7/PaperMatch_Analysis) and for the 3D map at [mitanshu7/arxiverse](https://github.com/mitanshu7/arxiverse).
