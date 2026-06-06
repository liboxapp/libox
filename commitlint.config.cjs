module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [
      1,
      'always',
      [
        'wiki',
        'decisions',
        'plan',
        'glosario',
        'compliance',
        'purchase',
        'draw',
        'delivery',
        'settlement',
        'ledger',
        'audit',
        'payments',
        'auth',
        'backoffice',
        'infra',
        'ci',
        'deps',
      ],
    ],
  },
};
