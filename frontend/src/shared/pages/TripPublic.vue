export default {
  async setup(props) {
    const route = useRoute()
    const { data: trip } = await useFetch(`/api/trips/${route.params.id}/`)
    return { trip }
  }
}