evaluation_dataset = [
    {
        "question": (
            "What should be validated before handing a newly provisioned "
            "enterprise environment back for live traffic?"
        ),
        "relevant_document_ids": [
            "dsid_7a9d6810cee2497f93113afa7feb0076"
        ],
        "reference_answer": (
            "Validate baseline latency and throughput, fallback and model "
            "switchover behavior, cache behavior where applicable, "
            "observability and alerting, rollback criteria, ownership, "
            "and escalation procedures."
        ),
    },
    {
        "question": (
            "What should be checked when troubleshooting NAT or egress "
            "exhaustion during cross-account GPU bursting?"
        ),
        "relevant_document_ids": [
            "dsid_229dd48e9b1d466a81ebaffe3ec84469"
        ],
        "reference_answer": (
            "Check NAT gateway metrics, connection tracking exhaustion, "
            "SNAT port usage, and egress billing spikes. Canaries can be "
            "shifted to another egress path and burst concurrency can be "
            "temporarily rate limited."
        ),
    },
    {
        "question": (
            "What evidence should be available before promoting an "
            "application to its first production launch?"
        ),
        "relevant_document_ids": [
            "dsid_926174fc4900408c89c98abde46b7225"
        ],
        "reference_answer": (
            "Production readiness should include successful API requests, "
            "a fallback policy or explicit acknowledgement of no fallback, "
            "observability such as request IDs or tracing, quota or budget "
            "controls, and a pinned model version."
        ),
    },
    {
        "question": (
            "How should network connectivity be validated for a private "
            "enterprise deployment?"
        ),
        "relevant_document_ids": [
            "dsid_8382d90bd5dd46289c813112491c154d"
        ],
        "reference_answer": (
            "Validate DNS resolution, TCP and TLS connectivity, peering "
            "routes, firewall and security-group rules, and perform an "
            "end-to-end authenticated inference request."
        ),
    },
    {
        "question": (
            "What steps should be followed when investigating an enterprise "
            "billing dispute?"
        ),
        "relevant_document_ids": [
            "dsid_fac7fd13fd4e44e68b82985482e0f388"
        ],
        "reference_answer": (
            "Review usage records and possible double counting, reconcile "
            "the invoice against canonical usage data and the applicable "
            "rate card, document evidence, determine the remedy, obtain "
            "finance approval, communicate with the customer, and record "
            "the final resolution."
        ),
    },
]