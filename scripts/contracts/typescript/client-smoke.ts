import assert from "node:assert/strict";
import createClient from "openapi-fetch";
import type { components, paths } from "./generated/api.js";

// Validación de tipos: estos errores deben seguir siendo errores al regenerar.
const exact: components["schemas"]["Money"] = { amount: "9007199254740993", currency: "PEN" };
// @ts-expect-error El contrato no admite números JSON para Money.amount.
const invalid: components["schemas"]["Money"] = { amount: 2500, currency: "PEN" };
void invalid;
assert.equal(exact.amount, "9007199254740993");

const baseUrl = process.env.LIBOX_CONTRACT_MOCK_URL;
assert.ok(baseUrl?.startsWith("http://127.0.0.1:"), "Solo mock local de fixtures");
const api = createClient<paths>({ baseUrl, headers: { Authorization: "Bearer synthetic-fixture" } });
const uuid = "00000000-0000-4000-8000-000000000001";
const order = await api.POST("/orders", {
  params: { header: { "Idempotency-Key": "synthetic-attempt-1" } },
  body: { raffle_id: uuid, quantity: 1, use_refund_credit: false, device_id: uuid },
});
assert.equal(order.response.status, 201);
assert.equal(order.data?.gross_amount.amount, "2500");
assert.equal(order.response.headers.get("X-Libox-Mock"), "fixtures-only");
assert.equal(order.response.headers.get("X-Trace-Id"), order.data?.trace_id);

const raffle = await api.GET("/raffles/{raffle_ref}", {
  params: { path: { raffle_ref: "sorteo-prueba" } },
});
assert.equal(raffle.response.status, 200);
assert.ok(raffle.data?.prize_value.approved_value.amount);
const pricing = await api.POST("/public/pricing-simulator", {
  body: { market: "PE", target_net_amount: { amount: "2000", currency: "PEN" } },
});
assert.equal(pricing.response.status, 200);
assert.equal(typeof pricing.data?.max_days_to_payout, "number");
const settlement = await api.GET("/settlements/{id}", { params: { path: { id: uuid } } });
assert.ok(settlement.data);
const execution = await api.POST("/settlements/{id}/execute", {
  params: { path: { id: uuid }, header: { "Idempotency-Key": "synthetic-settlement-attempt" } },
  body: { expected_version: settlement.data.version },
});
assert.equal(execution.response.status, 200);
assert.equal(execution.data?.version, 2);
console.log("Tipos generados y cliente TypeScript: 5 intercambios HTTP de fixtures correctos.");
