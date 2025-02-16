// components/App.js
"use client";
import { Input } from "postcss";
import { ReactHTML, useEffect, useState } from "react";
const jarvisUI = () => {
    let currentElem: ReactHTML;
    const diff: { x: number; y: number } = { x: 0, y: 0 };
    const [userInput, setUserInput] = useState("");
    const [result, setResult] = useState("");
    const handleAsk = () => {
        if (userInput == "") {
            return;
        }
        setResult(`You asked: ${userInput}`);

        if (window.electron) {
            window.electron.sendToPython({ event: "toPython", message: userInput });
            window.electron.onFromPython((event, message) => {
                setResult(message);
            });
            setUserInput("");
        } else {
            console.error("Electron object is not available");
        }
        setUserInput("");
    };
    const draggElement = (e: React.MouseEvent<HTMLElement>) => {
        //calculate the position of draggint
        let offsetLeft = e.clientX - diff.x;
        let offsetTop = e.clientY - diff.y;
        currentElem.style.left = `${offsetLeft}px`;
        currentElem.style.top = `${offsetTop}px`;
    };
    useEffect(() => {
        const draggableElement = document.querySelectorAll(".draggable");
        window.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                document.querySelector("#button").click();
            }
        });

        window.addEventListener("mousemove", (e) => {
            let flag = e.target.tagName;
            if (flag == "HTML") {
                window.electron.sendToPython({
                    event: "setMouseIgnore",
                    message: true,
                });
            } else {
                window.electron.sendToPython({
                    event: "setMouseIgnore",
                    message: false,
                });
            }
        });
        draggableElement.forEach((element) => {
            element.addEventListener("mousedown", (e) => {
                currentElem = element;
                diff.x = e.clientX - element.getBoundingClientRect().left;
                diff.y = e.clientY - element.getBoundingClientRect().top;
                window.addEventListener("mousemove", draggElement);
                window.addEventListener("mouseup", () => {
                    window.removeEventListener("mousemove", draggElement);
                });
            });
        });
        //when mouse will drag
        // Cleanup: remove event listeners on unmount
        return () => {
            window.removeEventListener("mousedown", () => { });
            window.removeEventListener("mousemove", () => { });
            window.removeEventListener("keydown", () => { });
        };
    }, []);
    return (
        <div className="flex overflow-hidden bg-transparent text-white">
            <div className="draggable   p-4 bg-black  cursor-move">
                <h1 className="text-xl  font-bold">Jarvis Assistant</h1>
                <input
                    type="text"
                    placeholder="Ask Jarvis..."
                    value={userInput}
                    onChange={(e) => setUserInput(e.currentTarget.value)}
                    className="mt-2 p-2 border border-gray-300 rounded"
                />

                <button
                    onClick={handleAsk}
                    id="button"
                    className="mt-2 bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                >
                    AskJarvis
                </button>
            </div>

            <div
                id="result"
                className="mt-2  outline-blue-300  border  border-blue-400 draggable   max-w-[70vh] cursor-move  "
            >
                {result && (
                    <div className="m-5 ">
                        <div className="title text-orange-400 space-y-4">
                            <span>Response from Kara</span>
                            <hr />
                        </div>
                        <div className="contnet my-2">{result}</div>
                    </div>
                )}{" "}
            </div>
        </div>
    );
};
export default jarvisUI;
