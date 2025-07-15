import { computed, watchEffect, ref } from 'vue'

export default function useQuoteTotals(form) {
  const freeEachCost = ref(0)
  const totalCost    = ref(0)

  watchEffect(() => {
    // Remove .value since form is now reactive, not a ref
    const f = form
    
    // Add null checks to prevent errors
    if (!f) return
    
    const baseTotal =
      (+f.itinerary_cost        || 0) +
      (+f.comision_usuario      || 0) +
      (+f.comision_leader       || 0) +
      (+f.lunch_cost            || 0) +
      (+f.tips_cost             || 0)

    // free-each math
    const pax = +f.free_each
    if (pax !== 10 && pax !== 0 && baseTotal > 0) {
      freeEachCost.value =
        Math.round(((baseTotal * 10 / 11) * (pax + 1)) / pax) - baseTotal
    } else {
      freeEachCost.value = 0
    }

    let sum = baseTotal + (+freeEachCost.value || 0)
    if (f.charge_city_fee === 'YES')
      sum += +f.departure_city_cost || 0

    totalCost.value = +sum.toFixed(2)
  })

  return { totalCost, freeEachCost }
}