import express, { Request, Response } from "express";
import morgan from "morgan";

const app = express();

app.use(express.json());
app.use(morgan("dev"));

app.get("/", (req: Request, res: Response) => {
    res.send("running");
});

const port = 4000;

app.listen(port, async () => {
    console.log(`Server running at http://localhost:${port}`);
});
