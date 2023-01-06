<script>
import adminStorageService from "@/services/AdminStorage";
export default{
    async created() {
        adminStorageService.clearToken()
        this.$router.push('/');
    }
}
</script>