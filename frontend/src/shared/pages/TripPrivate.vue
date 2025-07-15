export default {
  async setup(props) {
    const route = useRoute()
    const { data: trip } = await useFetch(`/api/trips/private/${route.params.token}/`)
    return { trip }
  }
}