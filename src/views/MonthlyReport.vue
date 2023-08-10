<template>
    <div>
        <h1 class="mt-5">Monthly Report Generator</h1>
        <form @submit.prevent="generateMonthlyReport">
            <label for="year">Year:</label>
            <input v-model="year" type="number" id="year" class="form-control w-50 mx-auto" name="year" required>
            <br />
            <label for="month">Month:</label>
            <input v-model="month" type="number" id="month" class="form-control mx-auto w-50" name="month" min="1" max="12"
                required>
            <br />

            <button class="btn btn-success" type="submit">Generate Report</button>
        </form>

        <div v-if="reportUrl">
            <h2 class="mt-5">Report Generated and sent via your registered mail</h2>
            <!-- <a :href="reportUrl" download="monthly_report.html" target="_blank" class="mt-5 btn btn-primary">Download HTML
                Report</a> -->
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            year: '',
            month: '',
            reportUrl: null,
        };
    },
    methods: {
        async generateMonthlyReport() {

            if (this.year < 1900 || this.year > 9999 || this.month < 1 || this.month > 12) {
                console.error('Invalid year or month');
                return;
            }

            try {
                const access_token = localStorage.getItem('access_token');
                if (!access_token) {
                    console.error('User not authenticated. Please log in first.');
                    return;
                }

                const response = await axios.get(
                    `http://localhost:5000/generate_monthly_report/${this.year}/${this.month}`,
                    {
                        responseType: 'arraybuffer',
                        withCredentials: true,
                        headers: {
                            Authorization: `Bearer ${access_token}`,
                        },
                    }
                );

                if (response.data instanceof ArrayBuffer) {
                    const blob = new Blob([response.data], { type: 'application' });
                    this.reportUrl = URL.createObjectURL(blob);
                } else {
                    console.error('Invalid response from the server');
                    this.reportUrl = null;
                }

            } catch (error) {
                console.error('Error generating report:', error);
            }
        },
    },
};
</script>
