import assert from "node:assert/strict";
import createClient from "openapi-fetch";
import type { components, paths } from "./generated/api.js";

// Validación de tipos: estos errores deben seguir siendo errores al regenerar.
const exact: components["schemas"]["Money"] = { amount: "9007199254740993", currency: "PEN" };
// @ts-expect-error El contrato no admite números JSON para Money.amount.
const invalid: components["schemas"]["Money"] = { amount: 2500, currency: "PEN" };
void invalid;
assert.equal(exact.amount, "9007199254740993");
// A5: LIVE ya no es capacidad; las categorías P-C van en su propio campo.
const capabilities: components["schemas"]["CapabilitiesUpdate"] = {
  // @ts-expect-error LIVE retirado de enabled_raffle_types.
  enabled_raffle_types: ["LIVE"], enabled_categories: ["P_C1"], expected_version: 1,
  reason: "Motivo sintético documentado para la operación.",
};
void capabilities;
// A9: la atestación ya no acepta un firmante elegido por el cliente.
const attestation: components["schemas"]["AttestationRequest"] = {
  evidence_ids: ["00000000-0000-4000-8000-000000000001"], winner_confirmed: true,
  statement: "Atestación sintética de entrega documentada.",
  // @ts-expect-error second_signer_id retirado (SignatureRequest ATTEST_PC).
  second_signer_id: "00000000-0000-4000-8000-000000000001",
};
void attestation;

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
// Auxiliares: leer la versión desde la respuesta, nunca fabricarla en el cliente.
const valuation = await api.GET("/valuations/{id}", { params: { path: { id: uuid } } });
assert.ok(valuation.data);
const decision = await api.POST("/valuations/{id}/decisions", {
  params: { path: { id: uuid } },
  body: {
    expected_version: valuation.data.version,
    outcome: "APPROVED",
    approved_value: { amount: "2500", currency: "PEN" },
    reason: "Referencias vigentes y banda satisfecha.",
  },
});
assert.equal(decision.response.status, 201);
assert.equal(decision.data?.subject_version, 2);
const upload = await api.POST("/uploads", {
  params: { header: { "Idempotency-Key": "synthetic-upload-attempt" } },
  body: {
    purpose: "ROOM_EVIDENCE", target_id: uuid, content_type: "application/pdf",
    size_bytes: 20480, sha256: "0".repeat(64),
  },
});
assert.ok(upload.data);
// No se visita upload_url: el fixture solo describe la interfaz.
const completed = await api.POST("/uploads/{id}/complete", {
  params: { path: { id: upload.data.upload_id } },
  body: { expected_version: upload.data.version },
});
assert.equal(completed.data?.status, "QUARANTINED");
const signature = await api.GET("/signature-requests/{id}", { params: { path: { id: uuid } } });
assert.ok(signature.data);
const signed = await api.POST("/signature-requests/{id}/sign", {
  params: { path: { id: uuid } },
  body: { expected_version: signature.data.version, decision: "SIGN", reason: "Revisión independiente conforme." },
});
assert.equal(signed.data?.status, "SIGNED");
assert.ok(signature.data.eligible_signer_subroles.length > 0);
// A7: la decisión KYB usa la versión leída del cliente.
const client = await api.GET("/clients/{id}", { params: { path: { id: uuid } } });
assert.ok(client.data);
const kyb = await api.POST("/clients/{id}/kyb/decisions", {
  params: { path: { id: uuid } },
  body: { expected_version: client.data.version, outcome: "REJECTED", reason: "Documento societario vencido." },
});
assert.equal(kyb.response.status, 201);
assert.equal(kyb.data?.status, "RECORDED");
console.log("Tipos generados y cliente TypeScript: 13 intercambios HTTP de fixtures correctos.");
