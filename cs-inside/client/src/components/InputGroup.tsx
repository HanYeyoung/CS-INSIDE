import React from "react";
import cls from "classnames"; // Ensure you have this package installed (npm install clsx)

interface InputGroupProps {
    className?: string;
    type?: string;
    placeholder?: string; // Made optional
    value: string;
    error?: string; // Marked error as optional
    setValue: (value: string) => void;
}

const InputGroup: React.FC<InputGroupProps> = ({
    className = "mb-2",
    type = "text",
    placeholder = "",
    value,
    setValue,
    error,
}) => {
    return (
        <div className={className}>
            <input
                type={type}
                style={{ minWidth: 300 }}
                className={cls(
                    "w-full p-3 transition duration-200 border rounded bg-gray-50 focus:bg-white hover:bg-white",
                    {
                        "border-red-500": error,
                        "border-gray-400": !error,
                    }
                )}
                placeholder={placeholder}
                value={value}
                onChange={(e) => setValue(e.target.value)}
            />
            {error && <small className="font-medium text-red-500">{error}</small>}
        </div>
    );
};

export default InputGroup;
