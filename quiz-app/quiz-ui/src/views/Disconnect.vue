<script>
import adminStorageService from "@/services/AdminStorage";
export default{
    name: "Disconnect",
    async created() {
        console.log("Composant Disconnect 'created'")
        adminStorageService.clearToken()
        this.$router.push('/');
    }
}
</script>