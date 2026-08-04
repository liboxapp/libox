import type { Raffle } from '@/lib/raffle';

const HOUR_MS = 60 * 60 * 1000;

/**
 * Mock catalog for the first slice. `endsAt` is generated relative to `now`
 * so countdowns always look alive in demos. States are deliberately varied:
 * freshly launched, advanced, almost sold out, closing in hours, finished.
 */
export function buildMockRaffles(now: Date = new Date()): Raffle[] {
  const hoursFromNow = (hours: number) => new Date(now.getTime() + hours * HOUR_MS);

  return [
    {
      id: 'raf-001',
      slug: 'iphone-16-pro',
      title: 'iPhone 16 Pro 256 GB',
      prize: 'iPhone 16 Pro 256 GB color titanio',
      description:
        'Participa por el iPhone 16 Pro de 256 GB, nuevo y sellado, con garantía oficial de un año. El sorteo se ejecuta con prueba criptográfica verificable.',
      category: 'tecnologia',
      ticketPriceCents: 2000,
      totalTickets: 2500,
      soldTickets: 1830,
      endsAt: hoursFromNow(5 * 24),
      status: 'activa',
      organizer: { name: 'Tiendas Conecta SAC', ruc: '20512345678' },
    },
    {
      id: 'raf-002',
      slug: 'laptop-gamer-legion',
      title: 'Laptop gamer Lenovo Legion',
      prize: 'Lenovo Legion 5, RTX 4060, 16 GB RAM',
      description:
        'Una laptop gamer de alto rendimiento para trabajo y juego. Nueva, sellada y con garantía de tienda.',
      category: 'tecnologia',
      ticketPriceCents: 1500,
      totalTickets: 3000,
      soldTickets: 620,
      endsAt: hoursFromNow(12 * 24),
      status: 'activa',
      organizer: { name: 'GamerZone Perú EIRL', ruc: '20601234567' },
    },
    {
      id: 'raf-003',
      slug: 'playstation-5-bundle',
      title: 'PlayStation 5 + 2 juegos',
      prize: 'PS5 edición estándar con 2 juegos a elección',
      description:
        'Consola PlayStation 5 con lector de discos y dos juegos a elección del ganador. Quedan pocos tickets.',
      category: 'tecnologia',
      ticketPriceCents: 1000,
      totalTickets: 2000,
      soldTickets: 1980,
      endsAt: hoursFromNow(2 * 24),
      status: 'activa',
      organizer: { name: 'GamerZone Perú EIRL', ruc: '20601234567' },
    },
    {
      id: 'raf-004',
      slug: 'moto-honda-navi',
      title: 'Moto Honda Navi 2026',
      prize: 'Honda Navi 2026 0 km, tarjeta y SOAT',
      description:
        'Moto Honda Navi del año, cero kilómetros, con tarjeta de propiedad y SOAT incluidos. Entrega en Lima o provincia.',
      category: 'vehiculos',
      ticketPriceCents: 2500,
      totalTickets: 4000,
      soldTickets: 2400,
      endsAt: hoursFromNow(9 * 24),
      status: 'activa',
      organizer: { name: 'Autonort Selva SAC', ruc: '20487654321' },
    },
    {
      id: 'raf-005',
      slug: 'auto-kia-picanto',
      title: 'Auto Kia Picanto 2026',
      prize: 'Kia Picanto 2026 0 km full equipo',
      description:
        'El gran premio del año: un Kia Picanto 2026 cero kilómetros, full equipo, con todos los gastos de transferencia pagados.',
      category: 'vehiculos',
      ticketPriceCents: 5000,
      totalTickets: 10000,
      soldTickets: 3100,
      endsAt: hoursFromNow(30 * 24),
      status: 'activa',
      organizer: { name: 'Autonort Selva SAC', ruc: '20487654321' },
    },
    {
      id: 'raf-006',
      slug: 'viaje-cusco-para-dos',
      title: 'Cusco para dos, todo incluido',
      prize: 'Viaje a Cusco 4D/3N para 2 personas',
      description:
        'Vuelos, hotel 4 estrellas, tours a Machu Picchu y Valle Sagrado para dos personas. Fechas flexibles.',
      category: 'viajes',
      ticketPriceCents: 1200,
      totalTickets: 1500,
      soldTickets: 1120,
      endsAt: hoursFromNow(6 * 24),
      status: 'activa',
      organizer: { name: 'Andes Travel Group SAC', ruc: '20556677889' },
    },
    {
      id: 'raf-007',
      slug: 'punta-cana-7-noches',
      title: 'Punta Cana, 7 noches para dos',
      prize: 'Resort todo incluido en Punta Cana',
      description:
        'Siete noches en resort 5 estrellas todo incluido para dos personas, con vuelos desde Lima.',
      category: 'viajes',
      ticketPriceCents: 3000,
      totalTickets: 5000,
      soldTickets: 900,
      endsAt: hoursFromNow(21 * 24),
      status: 'activa',
      organizer: { name: 'Andes Travel Group SAC', ruc: '20556677889' },
    },
    {
      id: 'raf-008',
      slug: 'combo-cocina-refrigeradora',
      title: 'Cocina + refrigeradora Samsung',
      prize: 'Combo Samsung: cocina 6 hornillas + refrigeradora 384 L',
      description:
        'Renueva tu hogar: cocina de 6 hornillas y refrigeradora side-by-side Samsung, con delivery incluido.',
      category: 'hogar',
      ticketPriceCents: 800,
      totalTickets: 1200,
      soldTickets: 460,
      endsAt: hoursFromNow(10 * 24),
      status: 'activa',
      organizer: { name: 'Electrohogar del Norte SRL', ruc: '20334455667' },
    },
    {
      id: 'raf-009',
      slug: 'juego-de-sala-completo',
      title: 'Juego de sala completo',
      prize: 'Sofá 3-2-1 + mesa de centro + rack de TV',
      description:
        'Juego de sala moderno en tela antimanchas: sofá 3-2-1, mesa de centro y rack para TV de hasta 65".',
      category: 'hogar',
      ticketPriceCents: 1000,
      totalTickets: 1000,
      soldTickets: 720,
      endsAt: hoursFromNow(4 * 24),
      status: 'activa',
      organizer: { name: 'Electrohogar del Norte SRL', ruc: '20334455667' },
    },
    {
      id: 'raf-010',
      slug: 'diez-mil-soles-efectivo',
      title: 'S/ 10,000 en efectivo',
      prize: 'S/ 10,000 depositados en tu cuenta',
      description:
        'Diez mil soles transferidos directamente a la cuenta bancaria del ganador. Cierra hoy: últimas horas para participar.',
      category: 'efectivo',
      ticketPriceCents: 2000,
      totalTickets: 3000,
      soldTickets: 2650,
      endsAt: hoursFromNow(10),
      status: 'activa',
      organizer: { name: 'Fundación Impulsa Perú', ruc: '20112233445' },
    },
    {
      id: 'raf-011',
      slug: 'cinco-mil-soles-efectivo',
      title: 'S/ 5,000 en efectivo',
      prize: 'S/ 5,000 depositados en tu cuenta',
      description:
        'Cinco mil soles para lo que tú decidas, transferidos al ganador con constancia del sorteo verificable.',
      category: 'efectivo',
      ticketPriceCents: 1000,
      totalTickets: 1500,
      soldTickets: 610,
      endsAt: hoursFromNow(8 * 24),
      status: 'activa',
      organizer: { name: 'Fundación Impulsa Perú', ruc: '20112233445' },
    },
    {
      id: 'raf-012',
      slug: 'macbook-air-m4',
      title: 'MacBook Air M4',
      prize: 'MacBook Air 13" chip M4, 16 GB',
      description:
        'Sorteo finalizado. La MacBook Air M4 ya tiene dueña: felicitaciones a la ganadora, elegida con prueba criptográfica verificable.',
      category: 'tecnologia',
      ticketPriceCents: 1800,
      totalTickets: 2000,
      soldTickets: 2000,
      endsAt: hoursFromNow(-3 * 24),
      status: 'finalizada',
      organizer: { name: 'Tiendas Conecta SAC', ruc: '20512345678' },
      winner: { name: 'Rosa Q.', ticketNumber: 842 },
    },
  ];
}

export const mockRaffles: Raffle[] = buildMockRaffles();

export function getRaffleBySlug(slug: string): Raffle | undefined {
  return mockRaffles.find((raffle) => raffle.slug === slug);
}
