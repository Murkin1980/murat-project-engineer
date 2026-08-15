# Browser Evidence Acquisition role

Disposition: `REUSE_COMPONENT`.

Use ordinary API/search/HTTP retrieval first. Invoke a browser provider only when public JS rendering, navigation, pagination, filters, or browser state materially adds evidence.

```text
Research task -> normal web sufficient? -> yes: validate/normalize
                                    -> no: BrowserAcquisitionAdapter
                                           -> BrowserAct | Playwright | future provider
                                           -> raw evidence -> validate -> normalize -> deduplicate
```

Conceptual boundary only:

```ts
interface BrowserAcquisitionAdapter {
  acquire(task: BrowserAcquisitionTask): Promise<RawEvidenceBatch>
}
```

Initial policy:

- Data: `PUBLIC` only.
- Actions: `READ`, `NAVIGATE`, `EXTRACT`.
- Prohibited: private authentication, customer data, write/message/purchase/financial/destructive actions, access-control or CAPTCHA bypass.
- Domain rules, validation, scoring, deduplication, evidence storage, and decisions remain outside BrowserAct.
- BrowserAct is optional and replaceable; no product runtime may depend on it without a new approved experiment.

Business Discovery mapping is compatible without core-model change: BrowserAct record -> Raw Evidence -> Validator -> Normalized Evidence -> EvidenceScore/Opportunity.
