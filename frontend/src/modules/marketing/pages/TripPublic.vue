<template>
  <TripTemplate :trip="trip" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import TripTemplate from '../components/TripTemplate.vue'
import http from '@/shared/services/http'

const route = useRoute()
const trip = ref({})
const loading = ref(true)
const error = ref(null)

const loadTrip = async () => {
  try {
    loading.value = true
    const slug = route.params.slug
    
    // Call the API to get trip data
    const response = await http.get(`/api/marketing/trips/${slug}/`)
    
    if (response.data && response.data.trip) {
      trip.value = response.data.trip
    } else {
      console.log('No trip data found in API response, using fallback mock data')
      // Fallback to mock data for development
      trip.value = {
        trip_title: '10 DAYS HOLY LAND',
        promo_text: 'Experience the journey of a lifetime through the Holy Land, where ancient history meets profound spirituality. Walk in the footsteps of Jesus Christ as you explore sacred sites that have drawn pilgrims for centuries. From the bustling streets of Jerusalem\'s Old City to the tranquil shores of the Sea of Galilee, this transformative pilgrimage will deepen your faith and create memories that will last forever. Join fellow believers in daily Mass, meaningful reflection, and spiritual growth as you discover the land where Christianity was born.',
        hero_image: 'https://gotravel.qodeinteractive.com/wp-content/uploads/2016/10/single-title-image-1.jpg',
        total_cost: '4560',
        departure_city: 'Los Angeles',
        departure_date: '2025-10-03',
        arrival_date: '2025-10-13',
        spiritual_director: 'John Pascuale',
        destination: { name: 'Holy Land' },
        trip_includes: 'Round-trip airfare from Los Angeles\n9 nights accommodation in 4-star hotels\nDaily breakfast and dinner\nProfessional English-speaking tour guide\nEntrance fees to all mentioned sites\nTransportation in air-conditioned coach\nBoat ride on Sea of Galilee\nCable car to Masada\nAirport transfers\nSpiritual director throughout the journey\nDaily Mass celebrations\nGroup travel insurance',
        trip_not_includes: 'Lunches (unless specified)\nPersonal expenses and souvenirs\nLaundry services\nBeverages with meals\nTips for guide and driver\nSingle room supplement ($650)\nTravel insurance (optional)\nVisa fees (if required)\nPre/post tour accommodation\nOptional excursions\nPhone calls and internet\nMedical expenses',
        video_link: 'https://www.youtube.com/embed/UFYoatJVXm8',
        brochure: '/images/brochure.webp',
        contact_info: 'Phone: +1 (555) 123-4567, Email: info@vizitor.com',
        itinerary: [
          {
            day: 1,
            title: 'Arrival in Tel Aviv & Transfer to Jerusalem',
            description: 'Arrive at Ben Gurion Airport, meet your guide, and transfer to Jerusalem. Evening orientation and welcome dinner at the hotel.',
            expanded: true
          },
          {
            day: 2,
            title: 'Old City of Jerusalem',
            description: 'Explore the Old City: Western Wall, Via Dolorosa, Church of the Holy Sepulchre, and the Jewish, Christian, Muslim, and Armenian Quarters.',
            expanded: false
          },
          {
            day: 3,
            title: 'Mount of Olives & Bethlehem',
            description: 'Visit the Mount of Olives, Garden of Gethsemane, and Church of All Nations. Afternoon trip to Bethlehem: Church of the Nativity and Shepherds\' Field.',
            expanded: false
          },
          {
            day: 4,
            title: 'Ein Karem & Yad Vashem',
            description: 'Morning visit to Ein Karem (birthplace of John the Baptist) and the Church of the Visitation. Afternoon at Yad Vashem Holocaust Memorial.',
            expanded: false
          },
          {
            day: 5,
            title: 'Dead Sea & Masada',
            description: 'Descend to the Dead Sea region. Ascend Masada by cable car, tour the ancient fortress, and float in the Dead Sea.',
            expanded: false
          },
          {
            day: 6,
            title: 'Galilee - Nazareth & Cana',
            description: 'Travel north to Nazareth: visit the Basilica of the Annunciation and St. Joseph\'s Church. Stop in Cana, site of Jesus\' first miracle.',
            expanded: false
          },
          {
            day: 7,
            title: 'Sea of Galilee & Capernaum',
            description: 'Boat ride on the Sea of Galilee. Visit Capernaum, Mount of Beatitudes, Tabgha (loaves and fishes), and the Primacy of Peter.',
            expanded: false
          },
          {
            day: 8,
            title: 'Mount Tabor & Jordan River',
            description: 'Ascend Mount Tabor, site of the Transfiguration. Afternoon renewal of baptismal vows at the Jordan River (Yardenit).',
            expanded: false
          },
          {
            day: 9,
            title: 'Haifa, Akko & Caesarea',
            description: 'Visit the Baha\'i Gardens in Haifa, Crusader city of Akko, and the Roman ruins of Caesarea Maritima on the Mediterranean coast.',
            expanded: false
          },
          {
            day: 10,
            title: 'Jaffa & Departure',
            description: 'Morning stroll through the ancient port city of Jaffa. Free time for shopping or reflection. Transfer to Ben Gurion Airport for departure.',
            expanded: false
          }
        ]
      }
    }
  } catch (err) {
    console.error('Error loading trip:', err)
    error.value = 'Failed to load trip details'
    
    // Use mock data as fallback
    trip.value = {
      trip_title: '10 DAYS HOLY LAND',
      promo_text: 'Experience the journey of a lifetime through the Holy Land, where ancient history meets profound spirituality. Walk in the footsteps of Jesus Christ as you explore sacred sites that have drawn pilgrims for centuries. From the bustling streets of Jerusalem\'s Old City to the tranquil shores of the Sea of Galilee, this transformative pilgrimage will deepen your faith and create memories that will last forever. Join fellow believers in daily Mass, meaningful reflection, and spiritual growth as you discover the land where Christianity was born.',
      hero_image: 'https://gotravel.qodeinteractive.com/wp-content/uploads/2016/10/single-title-image-1.jpg',
      total_cost: '4560',
      departure_city: 'Los Angeles',
      departure_date: '2025-10-03',
      arrival_date: '2025-10-13',
      spiritual_director: 'John Pascuale',
      destination: { name: 'Holy Land' },
      trip_includes: 'Round-trip airfare from Los Angeles\n9 nights accommodation in 4-star hotels\nDaily breakfast and dinner\nProfessional English-speaking tour guide\nEntrance fees to all mentioned sites\nTransportation in air-conditioned coach\nBoat ride on Sea of Galilee\nCable car to Masada\nAirport transfers\nSpiritual director throughout the journey\nDaily Mass celebrations\nGroup travel insurance',
      trip_not_includes: 'Lunches (unless specified)\nPersonal expenses and souvenirs\nLaundry services\nBeverages with meals\nTips for guide and driver\nSingle room supplement ($650)\nTravel insurance (optional)\nVisa fees (if required)\nPre/post tour accommodation\nOptional excursions\nPhone calls and internet\nMedical expenses',
      video_link: 'https://www.youtube.com/embed/UFYoatJVXm8',
      brochure: '/images/brochure.webp',
      contact_info: 'Phone: +1 (555) 123-4567, Email: info@vizitor.com',
      itinerary: [
        {
          day: 1,
          title: 'Arrival in Tel Aviv & Transfer to Jerusalem',
          description: 'Arrive at Ben Gurion Airport, meet your guide, and transfer to Jerusalem. Evening orientation and welcome dinner at the hotel.',
          expanded: false
        },
        {
          day: 2,
          title: 'Jerusalem Old City',
          description: 'Visit the Western Wall, Temple Mount, Church of the Holy Sepulchre, and walk the Via Dolorosa. Experience the spiritual heart of three major religions.',
          expanded: false
        },
        {
          day: 3,
          title: 'Bethlehem & Ein Karem',
          description: 'Journey to Bethlehem to visit the Church of the Nativity and Manger Square. Afternoon visit to Ein Karem, birthplace of John the Baptist.',
          expanded: false
        },
        {
          day: 4,
          title: 'Dead Sea & Masada',
          description: 'Descend to the Dead Sea region. Ascend Masada by cable car, tour the ancient fortress, and float in the Dead Sea.',
          expanded: false
        },
        {
          day: 5,
          title: 'Galilee - Nazareth & Cana',
          description: 'Travel north to Nazareth: visit the Basilica of the Annunciation and St. Joseph\'s Church. Stop in Cana, site of Jesus\' first miracle.',
          expanded: false
        },
        {
          day: 6,
          title: 'Sea of Galilee & Capernaum',
          description: 'Boat ride on the Sea of Galilee. Visit Capernaum, Mount of Beatitudes, Tabgha (loaves and fishes), and the Primacy of Peter.',
          expanded: false
        },
        {
          day: 7,
          title: 'Mount Tabor & Jordan River',
          description: 'Ascend Mount Tabor, site of the Transfiguration. Afternoon renewal of baptismal vows at the Jordan River (Yardenit).',
          expanded: false
        },
        {
          day: 8,
          title: 'Haifa, Akko & Caesarea',
          description: 'Visit the Baha\'i Gardens in Haifa, Crusader city of Akko, and the Roman ruins of Caesarea Maritima on the Mediterranean coast.',
          expanded: false
        },
        {
          day: 9,
          title: 'Jaffa & Free Time',
          description: 'Morning stroll through the ancient port city of Jaffa. Afternoon free time for shopping, reflection, or optional excursions.',
          expanded: false
        },
        {
          day: 10,
          title: 'Jerusalem & Departure',
          description: 'Final morning in Jerusalem for last-minute shopping or personal reflection. Transfer to Ben Gurion Airport for departure.',
          expanded: false
        }
      ]
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTrip()
})
</script>

<style scoped>
/* Any additional styles specific to this page */
</style>
