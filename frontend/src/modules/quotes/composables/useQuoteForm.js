import { ref, reactive, watch, onMounted } from 'vue'
import useQuoteTotals from './useQuoteTotals'
import http from '@/shared/services/http'

export default function useQuoteForm () {
  const currentUser = ref({ username: 'Loading...' })
  
  // Use reactive() instead of plain object to make it properly reactive
  const form = reactive({
    church_name: '',
    leader_name: '',
    departure_date: '',
    trip_name: '',
    itinerary_id: '',
    destination_group: '',
    departure_city_id: '',
    departure_city_cost: 0,
    charge_city_fee: 'NO',
    multi_city: false,
    multiCities: Array.from({ length: 9 }, () => ({ cityId:'', cost:'' })),
    // Add missing required fields
    is_dmc: false,
    mkt_shiped: false,
    itinerary_cost: '',
    comision_usuario: '100',
    comision_leader: '',
    total_cost: '',
    total_cost_land_only: '',
    display_commission_fundraiser: 'NO',
    coordinator_name: '',
    coordinator_phone: '',
    coordinator_email: '',
    language: 'ENGLISH',
    single_room_price: '',
    minimum_deposit: '300',
    lunch_and_tip_includes: '',
    free_each: '10',
    free_each_cost: '',
    lunch_included: '',
    lunch_cost: '',
    tip_included: '',
    tips_cost: '',
    cancelation_terms: 'NO',
    max_pax: '',
    agreement_file: null,
    official_file: null,
    notes: '',
    workflow_status_rel: 10,
    quote_status: 1,
    client: null,
    user: null,
    // Marketing fields
    main_photo: null,
    spiritual_coordinator_photo: null,
    brochure_private: null,
    brochure_public: null,
    registration_form: null,
    video_link: '',
    terms_conditions_template: '',
    trip_includes: '',
    trip_not_includes: '',
    website_gallery_template: '',
    marketing_kit_location: '',
    marketing_kit_progress: 'pending',
    marketing_kit_shipped: 'NO',
    tracking_number: '',
    publish_on_website: 'NO',
    private_link: '',
    public_link: '',
     date_created: '',
    date_updated: '',
  })

  // Load current user
  async function loadCurrentUser() {
    try {
      const response = await http.get('/api/current-user/')
      currentUser.value = response.data
      form.user = response.data.id
    } catch (error) {
      console.error('Failed to load current user:', error)
      currentUser.value = { username: 'Unknown User', id: null }
    }
  }

  /* cascade lunch/tip logic exactly like original -------------------- */
  watch(() => form.lunch_and_tip_includes, val => {
    switch (val) {
      case '0': form.lunch_included='NO'; form.lunch_cost='';
                form.tip_included='NO';   form.tips_cost=''; break
      case '1': form.lunch_included='YES';form.tip_included='NO'; form.tips_cost=''; break
      case '2': form.lunch_included='NO'; form.lunch_cost='';    form.tip_included='YES'; break
      case '3': form.lunch_included='YES';form.tip_included='YES'; break
    }
  })

  /* totals composable ------------------------------------------------ */
  const { totalCost, freeEachCost } = useQuoteTotals(form)
  watch(totalCost, v => form.total_cost = v)
  watch(freeEachCost, v => form.free_each_cost = v)

  return {
    form,
    currentUser,
    loadCurrentUser
  }
}