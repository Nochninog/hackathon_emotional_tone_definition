const API_URL = import.meta.env.VITE_API_URL;

export default class UploadService{
    async create_upload(formData){
        const res = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData,
        });

        return res.json();
    }

    async get_all_files(){
        const res = await fetch(`${API_URL}/files`, {
            method: "GET"
        });

        const data = await res.json();
        return data;
    }
}