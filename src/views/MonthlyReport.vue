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
            <h2>Generated Report</h2>
            <!-- Change the button text and behavior to download HTML report -->
            <a :href="reportUrl" download="monthly_report.html" target="_blank" class="mt-5 btn btn-primary">Download HTML
                Report</a>


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
            reportUrl: null, // Initialize with null
        };
    },
    methods: {
        async generateMonthlyReport() {
            try {
                const access_token = localStorage.getItem('access_token');
                if (!access_token) {
                    console.error('User not authenticated. Please log in first.');
                    return;
                }

                const response = await axios.get(
                    `http://localhost:5000/generate_monthly_report/${this.year}/${this.month}`,
                    {
                        responseType: 'arraybuffer', // Change to arraybuffer
                        withCredentials: true,
                        headers: {
                            Authorization: `Bearer ${access_token}`,
                        },
                    }
                );

                if (response.data instanceof ArrayBuffer) { // Check if response data is an ArrayBuffer
                    // Display the PDF in a new browser tab
                    const blob = new Blob([response.data], { type: 'application/pdf' });
                    this.reportUrl = URL.createObjectURL(blob);
                } else {
                    console.error('Invalid PDF response from the server');
                    this.reportUrl = null; // Clear the report URL if it's not a PDF
                }

            } catch (error) {
                console.error('Error generating report:', error);
            }
        },

        openPDFReport() {
            if (this.reportUrl) {
                // Open the PDF report in a new browser tab
                const blob = new Blob([response], { type: 'application/pdf' });

            }
        },
        async downloadPDF() {
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
                    // Create a blob from the response data
                    const blob = new Blob([response.data], { type: 'application/pdf' });
                    // Create an object URL for the blob
                    const objectUrl = URL.createObjectURL(blob);
                    // Create a download link and simulate a click to trigger the download
                    const link = document.createElement('a');
                    link.href = objectUrl;
                    link.download = `monthly_report_${this.year}_${this.month}.pdf`;
                    link.click();
                } else {
                    console.error('Invalid PDF response from the server');
                }

            } catch (error) {
                console.error('Error generating report:', error);
            }
        },
    },
};
</script>
