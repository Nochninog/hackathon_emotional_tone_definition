const API_URL = import.meta.env.VITE_API_URL;

function formatDate(dateString) {
    const date = new Date(dateString);

    const months = [
        "янв.", "фев.", "мар.", "апр.", "май", "июн.",
        "июл.", "авг.", "сен.", "окт.", "ноя.", "дек."
    ];

    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();

    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${day} ${month} ${year} г. ${hours}:${minutes}`;
}

function applyDateFormatting(arr) {
    return arr.map(item => ({
        ...item,
        uploaded_at: formatDate(item.uploaded_at)
    }));
}

export default class UploadService{
    static async create_upload(formData){
        console.log(formData);
        const res = await fetch(`${API_URL}/uploads/`, {
            method: "POST",
            body: formData,
        });
        return res.json();
    }

    static async get_all_files(search){
        const url = new URL(`${API_URL}/uploads/`);

        url.searchParams.append("search", search);
        
        const res = await fetch(url, {
            method: "GET"
        });
        const data = await res.json();
        return applyDateFormatting(data);
    }

    

    static async get_file_by_id(id) {
    const url = new URL(`${API_URL}/uploads/${id}`);

    const res = await fetch(url, {
        method: "GET"
    });

    const data = await res.json();
    return applyDateFormatting(data);
}

}