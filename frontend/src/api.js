const API_BASE = import.meta.env.VITE_API_URL ?? ''

function buildDescriptorParams(query) {
  const p = new URLSearchParams()
  query.descriptors.forEach((d) => p.append('descriptors', d))
  query.brands.forEach((b) => p.append('brands', b))
  query.countries.forEach((c) => p.append('countries', c))
  query.popularity.forEach((v) => p.append('popularity', v))
  query.excludedDescriptors.forEach((d) => p.append('excluded_descriptors', d))
  if (query.rating > 0) p.set('rating', query.rating)
  return p
}

function buildVectorBody(vector, query) {
  return {
    search_vector: vector,
    descriptors: query.descriptors,
    ...(query.brands.length && { brands: query.brands }),
    ...(query.countries.length && { countries: query.countries }),
    ...(query.popularity.length && { popularity: query.popularity }),
    ...(query.excludedDescriptors.length && { excluded_descriptors: query.excludedDescriptors }),
    ...(query.rating > 0 && { rating: query.rating }),
  }
}

export async function searchByDescriptors(query) {
  const params = buildDescriptorParams(query)
  const res = await fetch(`${API_BASE}/api/v1/search/descriptors?${params}`)
  if (!res.ok) throw new Error(`Search failed: ${res.status}`)
  return res.json()
}

export async function searchByVector(vector, query) {
  const res = await fetch(`${API_BASE}/api/v1/search/vector`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(buildVectorBody(vector, query)),
  })
  if (!res.ok) throw new Error(`Search failed: ${res.status}`)
  return res.json()
}

export function transformFragrance(f) {
  return {
    name: f.name,
    brand: f.brand,
    gender: f.gender,
    descriptors: [
      ...(f.accords ?? []),
      ...(f.top_notes ?? []),
      ...(f.mid_notes ?? []),
      ...(f.base_notes ?? []),
    ],
    url: f.url ?? '',
    rating: f.rating,
    score: f.score,
    popularity: f.popularity ?? 0,
  }
}
