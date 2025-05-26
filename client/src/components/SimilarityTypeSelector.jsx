import React from "react";
import "../styles/admin/SegmentationTypeSelector.css";

const SimilarityTypeSelector = ({ selectedOption, setSelectedOption }) => {
    return (
        <div className="segmentation-type-selector">
            {/* <h4>Seleccione el tipo de Segementación:</h4> */}
            <div className="radio-group">
                <label>
                    <input
                        type="radio"
                        value="1"
                        checked={selectedOption === "1"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    DICE
                </label>
                <label>
                    <input
                        type="radio"
                        value="2"
                        checked={selectedOption === "2"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    IOU
                </label>
                <label>
                    <input
                        type="radio"
                        value="3"
                        checked={selectedOption === "1"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    FID
                </label>
                <label>
                    <input
                        type="radio"
                        value="3"
                        checked={selectedOption === "1"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    PSNR
                </label>
                <label>
                    <input
                        type="radio"
                        value="3"
                        checked={selectedOption === "1"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    RESNET+COSENO
                </label>
            </div>
        </div>
    );
};

export default SimilarityTypeSelector;
