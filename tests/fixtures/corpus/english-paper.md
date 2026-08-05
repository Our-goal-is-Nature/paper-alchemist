# Abstract

Routing services must allocate limited teams while preserving service quality. Existing procedures often separate customer selection from route construction, which weakens global decisions. We introduce a neighborhood-guided search that coordinates both decisions through a unified representation. Experiments on public benchmark families compare the method with established baselines under identical limits. The verified study records consistent objective improvements and stable runtime behavior. These findings support joint optimization as a practical design principle.

# Introduction

Resource-constrained routing appears in emergency response, field service, and mobile collection systems. Decisions are difficult because selecting valuable requests changes the feasible routes, while route geometry changes which requests remain attractive. Prior studies have developed exact and heuristic procedures, but many procedures optimize these decisions in separate stages. This separation leaves a clear methodological gap when interactions are strong. The present study addresses that gap with a unified search representation. Its contributions are a coupled encoding, a targeted neighborhood, and a reproducible comparative evaluation.

# Related Work

Early routing studies emphasized exact formulations and bounding procedures [1]. Later metaheuristics improved scalability through population search, adaptive memory, and specialized neighborhoods [2]. A related stream studied profit-collecting variants, but frequently treated assignment and sequencing as loosely connected operations [3]. The literature therefore provides strong components without a common mechanism for preserving their interactions. Our design combines these insights while directly representing the coupled decision.

# Problem Definition

The problem is defined on a weighted graph with a depot, candidate customers, and a fixed set of teams. Each customer has a verified reward, and every traversed edge has a travel cost. A feasible solution contains one route per team and visits each selected customer at most once. The objective maximizes collected reward subject to the stated route limits. No additional capacity, time-window, or stochastic assumption is introduced unless it appears in the research context.

# Methodology

The method maintains a population of complete multi-route solutions. A constructive procedure first produces feasible candidates. The search then alternates between a coupled insertion neighborhood and a route-level exchange neighborhood. An adaptive score selects neighborhoods according to recent verified improvements. After local optimization, a diversity-aware replacement rule retains strong solutions without collapsing the population. Each component addresses a specific interaction identified in the problem analysis.

# Experiment Setup

The evaluation uses the benchmark families and baseline methods supplied in the study context. Every method receives the same stopping rule and is executed with the recorded random seeds. Objective value is the primary metric, while runtime and stability provide complementary evidence. Parameter values are fixed before the final comparison. Hardware, compiler settings, and statistical procedures are reported only when verified by the context.

# Results Analysis

The reported results first establish the overall comparison and then examine where the difference arises. Aggregate tables distinguish best, average, and dispersion measures. Pairwise statements include a verified magnitude rather than relying only on rank. Component experiments connect each ablation to its algorithmic role. Observations are separated from explanations, and explanations are qualified when the experiment does not establish causality.

# Conclusion

The study addresses coupled selection and routing through a unified search design. Verified experiments show how the method compares with the supplied baselines and which components contribute to its behavior. The conclusion restates only evidence established by the study, acknowledges supplied limitations, and proposes future work only when it follows from those limitations. The broader implication is framed as a supported design lesson rather than a universal claim.
