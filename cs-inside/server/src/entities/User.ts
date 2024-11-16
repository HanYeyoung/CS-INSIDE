import { IsEmail, Length } from "class-validator";
import { Entity, PrimaryGeneratedColumn, Column, Index, OneToMany } from "typeorm";
import bcrypt from 'bcryptjs';
import Post from "./Post";
import Vote from "./Vote";

@Entity("users")
export class User {

    @Index()
    @IsEmail(undefined, {message: "Email address is wrong"})
    @Length(1,255, {message: "Email address cannot be empty"})
    @Column({ unique: true })
    email: string;

    @Index()
    @Length(3, 32, {message: "User name should be longer than 3 letters"})
    @Column({ unique: true })
    username: string

    @Column()
    @Length(6, 255, {message: "Password shoule be more than 6 letters"})
    lastName: string

    @OneToMany(() => Post, (post) => post.user)
    posts: Post[]

    @OneToMany(() => Vote, (vote) => vote.user)
    votes: Vote[]

    @BeforeInsert()
    async hashPassword() {
        this.password = await bcrypt.hash(this.hashPassword, 6)
    }
}
