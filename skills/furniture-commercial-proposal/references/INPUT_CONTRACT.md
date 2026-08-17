# Furniture КП Input Contract

## Minimum usable input per position

Required:

- product name;
- quantity;
- unit price;
- at least one source sketch/photo OR an explicit statement that no image exists.

Preferred:

- dimensions;
- material / decor;
- hardware / functional details;
- client name;
- date;
- notes/terms.

## Sequential intake example

User supplies position 1 -> acknowledge and store it -> ask for position 2.

Do not re-summarize the entire project after every upload. A short confirmation with the normalized position is enough.

## Conflict resolution

Priority:

1. User's latest explicit text instruction.
2. Earlier explicit user text.
3. Text visibly printed on the supplied sketch.
4. Visual inference.

If levels 1-3 conflict materially, ask before finalizing.

## Price rules

- Currency default is KZT only when the user is operating in the Kazakhstan furniture context or explicitly provides tenge prices.
- Show unit price prominently.
- When quantity > 1, keep the unit price label unambiguous.
- Do not show grand total by default in this canonical КП format.
- Do not calculate discounts, taxes, delivery, installation, or totals unless instructed.
