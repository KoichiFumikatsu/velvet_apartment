# Velvet Apartment — Diseño (GDD/spec)

- Fecha: 2026-07-17
- Estado: **diseño aprobado**, pendiente plan de implementación.
- Género: **idle / incremental** para adultos (+18) en **Ren'Py 8.3.7**.
- Arte: **IA Gen propio** (RunPod) — CG estáticos con efectos (ATL/parallax), no animación cuadro a cuadro.
- Distribución: **release público**. Elenco **"inspirado en" / fan-art legalmente distinto** (nombre propio distinto, diseño alterado, sin logos/nombres de franquicia; evitar calcar personajes de franquicias agresivas — HoYoverse/Genshin, Nintendo/Pokémon, etc.).

> Los valores numéricos son **iniciales y tunables**; están para poder implementar y balancear después, no son definitivos.

## 1. Pilares
- Idle relajado + **colección de contenido**. El dinero es el medio; los CG/eventos son el fin. La economía existe para **dosificar desbloqueos**.
- Ritmo **híbrido**: el hotel gana offline (con tope); jugando desbloqueas afecto/eventos/CG y el clicker da picos.
- Progresión vertical clara: subes de piso, el hotel crece, aparecen más huéspedes.

## 2. Bucle central
1. Habitaciones ocupadas generan **dinero/seg** (idle, incluido offline con tope).
2. Gastas dinero en: upgrades de habitación (↑ingreso), **fachada** global (multiplicador suave), reparaciones de piso (expansión) y **acondicionar** habitaciones (dispara la llegada de una huésped).
3. **Visitas** una habitación → interacción/evento → sube el **afecto** de esa huésped (activo).
4. El afecto (a) **multiplica el ingreso** de esa habitación y (b) cruza umbrales que **desbloquean tiers de contenido**.
5. Eventos de **paquete** abren el **clicker** → pico de dinero extra (acotado).
6. 3 habitaciones ocupadas + reparación pagada → **ascensor** al piso siguiente. Repite escalando.
7. (Endgame, post-MVP) Renovación/prestigio → **reputación (estrellas)** → multiplicador permanente; la galería queda desbloqueada.

## 3. Estructura del hotel
| Elemento | Regla |
|---|---|
| Piso | 3 habitaciones + ascensor |
| Habitación | vacía → (evento de llegada) ocupada → upgradeable por niveles |
| 3 primeras habitaciones | no se "compran"; se **acondicionan** (pago) y eso dispara la llegada de la huésped |
| Muro de piso | 3 ocupadas + coste de reparación (hito fijo) → desbloquea ascensor a piso N+1 |
| Piso 1 | la 1ª huésped es el **tutorial** |

## 4. Economía (fórmulas + valores iniciales)
- **Ingreso habitación** = `base_piso × nivel_upgrade × mult_afecto × mult_fachada`.
  - `base_piso`: piso 1 = 1.0 $/s (cada piso superior escala, p.ej. ×5 por piso).
- **Coste upgrade habitación** = `base × 1.15^nivel` (curva geométrica canónica). base inicial = 10 $.
- **Fachada** (global): coste = `100 × 1.5^nivel`; cada nivel = **+10% a todo el ingreso**. Suave, **sin decaimiento** (nunca se van las huéspedes por descuido).
- **Afecto** por huésped: rango 0–100.
  - `mult_afecto` = `1 + afecto/50` (afecto 0 → ×1, afecto 100 → ×3).
  - Sube por **visita/evento**: +5 por visita, cooldown 60 s (evita spam de clics).
  - **Servicios** pagados: empujón puntual (+10 afecto), coste geométrico `base × 1.3^compras`.
- **Clicker** (evento paquete): sesión de 15 s, cada clic = `0.5 × ingreso_total/s`, recompensa total topada a ~5 min de ingreso. Cooldown 10 min.
- **Offline**: al cargar, `now − last_seen` acredita dinero al ritmo pasivo, con **tope de 8 h**.

## 5. Afecto → contenido (4 tiers)
| Tier | Umbral afecto | Contenido |
|---|---|---|
| SFW | 0 | presentación, charla, arco |
| Suggestive | 25 | insinuante |
| NSFW | 60 | explícito |
| NSFW Nocturno | 90 | escenas nocturnas (tier tope) |

- Tipos de evento: **de afecto** (sube relación/desbloquea interacción), **de historia** (arco del personaje), **de dinero** (paquete → clicker; recompensa sugerente).
- **Galería**: los CG desbloqueados quedan guardados (retención + coleccionable).

## 6. Marco narrativo
- Intro VN: desempleado desesperado → oferta absurdamente bien pagada (sospechosa) → entrevista en lugar raro → se duerme → despierta en el **lobby** → **contrato ya firmado** en recepción (no recuerda firmarlo) → deber único: mantener satisfechas a las huéspedes → entra la **1ª huésped** (tutorial), personaje "inspirado en", el prota la reconoce.
- **Misterio del hotel/contrato**: hilo de fondo dosificado por hitos (cada piso revela un fragmento). Opcional para MVP (stubs).

## 7. Arquitectura técnica (Ren'Py 8.3.7)
| Pieza | Diseño |
|---|---|
| Datos | Clases Python `Guest`, `Room`, `Floor`; estado global (`dinero`, `fachada_nivel`, `reputacion`) en `store`. Huéspedes definidas por **datos** (tabla/JSON), no hardcode → añadir huéspedes IA Gen = datos + assets |
| Persistencia | Save nativo de Ren'Py (las vars en `store` se serializan) |
| Idle / offline | Timestamp real guardado; al cargar, `now − last_seen` → acreditar dinero con tope (8 h). Tick activo con `timer 1.0` en la screen principal |
| UI | `screen` principal = corte del hotel (pisos/habitaciones) con `imagebutton` por habitación; screens de habitación, upgrades, galería, clicker |
| CG + efectos | ATL/`transform` para parallax y transiciones; `layeredimage` para variaciones de personaje/tier |
| Separación | Lógica (economía/afecto) en `.py` puro y **testeable**; presentación en `.rpy` (screens) |

## 8. Alcance MVP (primer jugable)
- **Piso 1 completo**: 3 habitaciones, 3 huéspedes, tutorial con la 1ª.
- Bucle idle de dinero (con offline) + afecto por visita + fachada + **1 evento clicker** (paquete).
- Tiers **SFW + Suggestive** para las 3 huéspedes, y **al menos 1 huésped con los 4 tiers** completos (validar el arco entero).
- **Muro a piso 2** funcional (piso 2 = "próximamente").
- **Galería** básica.
- **Sin prestigio**.
- Objetivo: validar que el bucle *dinero → afecto → contenido → expansión* engancha antes de escalar pisos/huéspedes.

## 9. Fuera de alcance MVP (backlog)
Prestigio/reputación · pisos 2+ · misterio narrativo completo · balance fino de curvas · sonido/música · port Android.
