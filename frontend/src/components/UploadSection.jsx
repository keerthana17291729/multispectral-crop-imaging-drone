import { useState } from "react"
import { uploadImage } from "../services/api"

function UploadSection({ setResult, setFile }) {

    const [selected, setSelected] = useState(null)
    const [loading, setLoading] = useState(false)

    const handleFileChange = (e) => {
        setSelected(e.target.files[0])
    }

    const handleUpload = async () => {

        if (!selected) return

        setFile(selected)

        setLoading(true)

        const res = await uploadImage(selected)

        setResult(res)

        setLoading(false)

    }

    return (

        <div className="upload-box">

            <h2>Upload Crop Image</h2>

            <div className="upload-row">

                <input
                    className="choose-file"
                    type="file"
                    accept=".tif,.tiff"
                    onChange={handleFileChange}
                />

                <button onClick={handleUpload}>

                    {loading ? "Processing..." : "Upload"}

                </button>

            </div>

        </div>

    )

}

export default UploadSection